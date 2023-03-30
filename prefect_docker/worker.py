"""
<span class="badge-api beta"/>

Module containing the Docker worker used for executing flow runs as Docker containers.

Note this module is in **beta**. The interfaces within may change without notice.

To start a Docker worker, run the following command:

```bash
prefect worker start --pool 'my-work-pool' --type docker
```

Replace `my-work-pool` with the name of the work pool you want the worker
to poll for flow runs.

For more information about work pools and workers,
checkout out the [Prefect docs](https://docs.prefect.io/concepts/work-pools/).
"""
import enum
import re
import sys
import urllib.parse
import warnings
from typing import TYPE_CHECKING, Dict, Generator, List, Optional, Tuple

import anyio.abc
import packaging.version
import prefect
from prefect.docker import (
    format_outlier_version_name,
    get_prefect_image_name,
    parse_image_tag,
)
from prefect.experimental.workers.base import (
    BaseJobConfiguration,
    BaseWorker,
    BaseWorkerResult,
)
from prefect.settings import PREFECT_API_URL
from prefect.utilities.asyncutils import run_sync_in_worker_thread
from prefect.utilities.importtools import lazy_import
from pydantic import Field, validator
from slugify import slugify
from typing_extensions import Literal

if TYPE_CHECKING:
    import docker
    from docker import DockerClient
    from docker.models.containers import Container
    from prefect.client.schemas import FlowRun
    from prefect.server.schemas.core import Flow
    from prefect.server.schemas.responses import DeploymentResponse
else:
    docker = lazy_import("docker")

CONTAINER_LABELS = {
    "io.prefect.version": prefect.__version__,
}


class ImagePullPolicy(enum.Enum):
    """Enum representing the image pull policy options for a Docker container."""

    IF_NOT_PRESENT = "IfNotPresent"
    ALWAYS = "Always"
    NEVER = "Never"


class DockerWorkerJobConfiguration(BaseJobConfiguration):
    """
    Configuration class used by the Docker worker.

    An instance of this class is passed to the Docker worker's `run` method
    for each flow run. It contains all the information necessary to execute the
    flow run as a Docker container.

    Attributes:
        name: The name to give to created Docker containers.
        command: The command executed in created Docker containers to kick off
            flow run execution.
        env: The environment variables to set in created Docker containers.
        labels: The labels to set on created Docker containers.
        image: The image reference of a container image to use for created jobs.
            If not set, the latest Prefect image will be used.
        image_pull_policy: The image pull policy to use when pulling images.
        networks: Docker networks that created containers should be connected to.
        network_mode: The network mode for the created containers (e.g. host, bridge).
            If 'networks' is set, this cannot be set.
        auto_remove: If set, containers will be deleted on completion.
        volumes: Docker volumes that should be mounted in created containers.
        stream_output: If set, the output from created containers will be streamed
            to local standard output.
        mem_limit: Memory limit of created containers. Accepts a value
            with a unit identifier (e.g. 100000b, 1000k, 128m, 1g.) If a value is
            given without a unit, bytes are assumed.
        memswap_limit: Total memory (memory + swap), -1 to disable swap. Should only be
            set if `mem_limit` is also set. If `mem_limit` is set, this defaults to
            allowing the container to use as much swap as memory. For example, if
            `mem_limit` is 300m and `memswap_limit` is not set, containers can use
            600m in total of memory and swap.
        privileged: Give extended privileges to created containers.
    """

    image: str = Field(
        default_factory=get_prefect_image_name,
        description="The image reference of a container image to use for created jobs. "
        "If not set, the latest Prefect image will be used.",
        example="docker.io/prefecthq/prefect:2-latest",
    )
    image_pull_policy: Optional[Literal["IfNotPresent", "Always", "Never"]] = Field(
        default=None,
        description="The image pull policy to use when pulling images.",
    )
    networks: List[str] = Field(
        default_factory=list,
        description="Docker networks that created containers should be connected to.",
    )
    network_mode: Optional[str] = Field(
        default=None,
        description=(
            "The network mode for the created containers (e.g. host, bridge). If"
            " 'networks' is set, this cannot be set."
        ),
    )
    auto_remove: bool = Field(
        default=False,
        description="If set, containers will be deleted on completion.",
    )
    volumes: List[str] = Field(
        default_factory=list,
        description="A list of volume to mount into created containers.",
        example=["/my/local/path:/path/in/container"],
    )
    stream_output: bool = Field(
        default=True,
        description=(
            "If set, the output from created containers will be streamed to local "
            "standard output."
        ),
    )
    mem_limit: Optional[str] = Field(
        default=None,
        title="Memory Limit",
        description=(
            "Memory limit of created containers. Accepts a value "
            "with a unit identifier (e.g. 100000b, 1000k, 128m, 1g.) "
            "If a value is given without a unit, bytes are assumed."
        ),
    )
    memswap_limit: Optional[str] = Field(
        default=None,
        title="Memory Swap Limit",
        description=(
            "Total memory (memory + swap), -1 to disable swap. Should only be "
            "set if `mem_limit` is also set. If `mem_limit` is set, this defaults to"
            "allowing the container to use as much swap as memory. For example, if "
            "`mem_limit` is 300m and `memswap_limit` is not set, containers can use "
            "600m in total of memory and swap."
        ),
    )

    privileged: bool = Field(
        default=False,
        description="Give extended privileges to created container.",
    )

    @validator("volumes")
    def _validate_volume_format(cls, volumes):
        """Validates that provided volume strings are in the correct format."""
        for volume in volumes:
            if ":" not in volume:
                raise ValueError(
                    "Invalid volume specification. "
                    f"Expected format 'path:container_path', but got {volume!r}"
                )

        return volumes

    def _convert_labels_to_docker_format(self, labels: Dict[str, str]):
        """Converts labels to the format expected by Docker."""
        labels = labels or {}
        new_labels = {}
        for name, value in labels.items():
            if "/" in name:
                namespace, key = name.split("/", maxsplit=1)
                new_namespace = ".".join(reversed(namespace.split(".")))
                new_labels[f"{new_namespace}.{key}"] = value
            else:
                new_labels[name] = value
        return new_labels

    def _slugify_container_name(self) -> Optional[str]:
        """
        Generates a container name to match the configured name, ensuring it is Docker
        compatible.
        """
        # Must match `/?[a-zA-Z0-9][a-zA-Z0-9_.-]+` in the end
        if not self.name:
            return None

        return (
            slugify(
                self.name,
                lowercase=False,
                # Docker does not limit length but URL limits apply eventually so
                # limit the length for safety
                max_length=250,
                # Docker allows these characters for container names
                regex_pattern=r"[^a-zA-Z0-9_.-]+",
            ).lstrip(
                # Docker does not allow leading underscore, dash, or period
                "_-."
            )
            # Docker does not allow 0 character names so cast to null if the name is
            # empty after slufification
            or None
        )

    def _base_environment(self):
        """
        If the API URL has been set update the value to ensure connectivity
        when using a bridge network by updating local connections to use the
        docker internal host unless the network mode is "host" where localhost
        is available already.
        """

        base_env = super()._base_environment()
        network_mode = self.get_network_mode()
        if (
            "PREFECT_API_URL" in base_env
            and base_env["PREFECT_API_URL"] is not None
            and network_mode != "host"
        ):
            base_env["PREFECT_API_URL"] = (
                base_env["PREFECT_API_URL"]
                .replace("localhost", "host.docker.internal")
                .replace("127.0.0.1", "host.docker.internal")
            )
        return base_env

    def prepare_for_flow_run(
        self,
        flow_run: "FlowRun",
        deployment: Optional["DeploymentResponse"] = None,
        flow: Optional["Flow"] = None,
    ):
        """
        Prepares the agent for a flow run by setting the image, labels, and name
        attributes.
        """
        super().prepare_for_flow_run(flow_run, deployment, flow)

        self.image = self.image or get_prefect_image_name()
        self.labels = self._convert_labels_to_docker_format(
            {**self.labels, **CONTAINER_LABELS}
        )
        self.name = self._slugify_container_name()

    def get_network_mode(self) -> Optional[str]:
        """
        Returns the network mode to use for the container based on the configured
        options and the platform.
        """
        # User's value takes precedence; this may collide with the incompatible options
        # mentioned below.
        if self.network_mode:
            if sys.platform != "linux" and self.network_mode == "host":
                warnings.warn(
                    f"{self.network_mode!r} network mode is not supported on platform "
                    f"{sys.platform!r} and may not work as intended."
                )
            return self.network_mode

        # Network mode is not compatible with networks or ports (we do not support ports
        # yet though)
        if self.networks:
            return None

        # Check for a local API connection
        api_url = self.env.get("PREFECT_API_URL", PREFECT_API_URL.value())

        if api_url:
            try:
                _, netloc, _, _, _, _ = urllib.parse.urlparse(api_url)
            except Exception as exc:
                warnings.warn(
                    f"Failed to parse host from API URL {api_url!r} with exception: "
                    f"{exc}\nThe network mode will not be inferred."
                )
                return None

            host = netloc.split(":")[0]

            # If using a locally hosted API, use a host network on linux
            if sys.platform == "linux" and (host == "127.0.0.1" or host == "localhost"):
                return "host"

        # Default to unset
        return None

    def get_extra_hosts(self, docker_client) -> Optional[Dict[str, str]]:
        """
        A host.docker.internal -> host-gateway mapping is necessary for communicating
        with the API on Linux machines. Docker Desktop on macOS will automatically
        already have this mapping.
        """
        if sys.platform == "linux" and (
            # Do not warn if the user has specified a host manually that does not use
            # a local address
            "PREFECT_API_URL" not in self.env
            or re.search(
                ".*(localhost)|(127.0.0.1)|(host.docker.internal).*",
                self.env["PREFECT_API_URL"],
            )
        ):
            user_version = packaging.version.parse(
                format_outlier_version_name(docker_client.version()["Version"])
            )
            required_version = packaging.version.parse("20.10.0")

            if user_version < required_version:
                warnings.warn(
                    "`host.docker.internal` could not be automatically resolved to"
                    " your local ip address. This feature is not supported on Docker"
                    f" Engine v{user_version}, upgrade to v{required_version}+ if you"
                    " encounter issues."
                )
                return {}
            else:
                # Compatibility for linux -- https://github.com/docker/cli/issues/2290
                # Only supported by Docker v20.10.0+ which is our minimum recommend
                # version
                return {"host.docker.internal": "host-gateway"}

    def _determine_image_pull_policy(self) -> ImagePullPolicy:
        """
        Determine the appropriate image pull policy.

        1. If they specified an image pull policy, use that.

        2. If they did not specify an image pull policy and gave us
           the "latest" tag, use ImagePullPolicy.always.

        3. If they did not specify an image pull policy and did not
           specify a tag, use ImagePullPolicy.always.

        4. If they did not specify an image pull policy and gave us
           a tag other than "latest", use ImagePullPolicy.if_not_present.

        This logic matches the behavior of Kubernetes.
        See:https://kubernetes.io/docs/concepts/containers/images/#imagepullpolicy-defaulting
        """
        if not self.image_pull_policy:
            _, tag = parse_image_tag(self.image)
            if tag == "latest" or not tag:
                return ImagePullPolicy.ALWAYS
            return ImagePullPolicy.IF_NOT_PRESENT
        return ImagePullPolicy(self.image_pull_policy)


class DockerWorkerResult(BaseWorkerResult):
    """Contains information about a completed Docker container"""


class DockerWorker(BaseWorker):
    """Prefect worker that executes flow runs within Docker containers."""

    type = "docker"
    job_configuration = DockerWorkerJobConfiguration

    async def run(
        self,
        flow_run: "FlowRun",
        configuration: BaseJobConfiguration,
        task_status: Optional[anyio.abc.TaskStatus] = None,
    ) -> BaseWorkerResult:
        """
        Executes a flow run within a Docker container and waits for the flow run
        to complete.
        """
        # The `docker` library uses requests instead of an async http library so it must
        # be run in a thread to avoid blocking the event loop.
        container = await run_sync_in_worker_thread(
            self._create_and_start_container, configuration
        )
        container_pid = self._get_infrastructure_pid(container_id=container.id)

        # Mark as started and return the infrastructure id
        if task_status:
            task_status.started(container_pid)

        # Monitor the container
        container = await run_sync_in_worker_thread(
            self._watch_container_safe, container, configuration
        )

        exit_code = container.attrs["State"].get("ExitCode")
        return DockerWorkerResult(
            status_code=exit_code if exit_code is not None else -1,
            identifier=container_pid,
        )

    def _get_client(self):
        """Returns a docker client."""
        try:
            with warnings.catch_warnings():
                # Silence warnings due to use of deprecated methods within dockerpy
                # See https://github.com/docker/docker-py/pull/2931
                warnings.filterwarnings(
                    "ignore",
                    message="distutils Version classes are deprecated.*",
                    category=DeprecationWarning,
                )

                docker_client = docker.from_env()

        except docker.errors.DockerException as exc:
            raise RuntimeError("Could not connect to Docker.") from exc

        return docker_client

    def _get_infrastructure_pid(self, container_id: str) -> str:
        """Generates a Docker infrastructure_pid string in the form of
        `<docker_host_base_url>:<container_id>`.
        """
        docker_client = self._get_client()
        base_url = docker_client.api.base_url
        docker_client.close()
        return f"{base_url}:{container_id}"

    def _parse_infrastructure_pid(self, infrastructure_pid: str) -> Tuple[str, str]:
        """Splits a Docker infrastructure_pid into its component parts"""

        # base_url can contain `:` so we only want the last item of the split
        base_url, container_id = infrastructure_pid.rsplit(":", 1)
        return base_url, str(container_id)

    def _build_container_settings(
        self,
        docker_client: "DockerClient",
        configuration: DockerWorkerJobConfiguration,
    ) -> Dict:
        """Builds a dictionary of container settings to pass to the Docker API."""
        network_mode = configuration.get_network_mode()
        return dict(
            image=configuration.image,
            network=configuration.networks[0] if configuration.networks else None,
            network_mode=network_mode,
            command=configuration.command,
            environment=configuration.env,
            auto_remove=configuration.auto_remove,
            labels=configuration.labels,
            extra_hosts=configuration.get_extra_hosts(docker_client),
            name=configuration.name,
            volumes=configuration.volumes,
            mem_limit=configuration.mem_limit,
            memswap_limit=configuration.memswap_limit,
            privileged=configuration.privileged,
        )

    def _create_and_start_container(
        self, configuration: DockerWorkerJobConfiguration
    ) -> "Container":
        """Creates and starts a Docker container."""
        docker_client = self._get_client()
        container_settings = self._build_container_settings(
            docker_client, configuration
        )

        if self._should_pull_image(docker_client, configuration=configuration):
            self._logger.info(f"Pulling image {configuration.image!r}...")
            self._pull_image(docker_client, configuration)

        container = self._create_container(docker_client, **container_settings)

        # Add additional networks after the container is created; only one network can
        # be attached at creation time
        if len(configuration.networks) > 1:
            for network_name in configuration.networks[1:]:
                network = docker_client.networks.get(network_name)
                network.connect(container)

        # Start the container
        container.start()

        docker_client.close()

        return container

    def _watch_container_safe(
        self, container: "Container", configuration: DockerWorkerJobConfiguration
    ) -> "Container":
        """Watches a container for completion, handling any errors that may occur."""
        # Monitor the container capturing the latest snapshot while capturing
        # not found errors
        docker_client = self._get_client()

        try:
            for latest_container in self._watch_container(
                docker_client, container.id, configuration
            ):
                container = latest_container
        except docker.errors.NotFound:
            # The container was removed during watching
            self._logger.warning(
                f"Docker container {container.name} was removed before we could wait "
                "for its completion."
            )
        finally:
            docker_client.close()

        return container

    def _watch_container(
        self,
        docker_client: "DockerClient",
        container_id: str,
        configuration: DockerWorkerJobConfiguration,
    ) -> Generator[None, None, "Container"]:
        """
        Watches a container for completion, yielding the latest container
        snapshot on each iteration.
        """
        container: "Container" = docker_client.containers.get(container_id)

        status = container.status
        self._logger.info(
            f"Docker container {container.name!r} has status {container.status!r}"
        )
        yield container

        if configuration.stream_output:
            try:
                for log in container.logs(stream=True):
                    log: bytes
                    print(log.decode().rstrip())
            except docker.errors.APIError as exc:
                if "marked for removal" in str(exc):
                    self._logger.warning(
                        f"Docker container {container.name} was marked for removal"
                        " before logs could be retrieved. Output will not be"
                        " streamed. "
                    )
                else:
                    self._logger.exception(
                        "An unexpected Docker API error occured while streaming output "
                        f"from container {container.name}."
                    )

            container.reload()
            if container.status != status:
                self._logger.info(
                    f"Docker container {container.name!r} has status"
                    f" {container.status!r}"
                )
            yield container

        container.wait()
        self._logger.info(
            f"Docker container {container.name!r} has status {container.status!r}"
        )
        yield container

    def _should_pull_image(
        self, docker_client: "DockerClient", configuration: DockerWorkerJobConfiguration
    ) -> bool:
        """
        Decide whether we need to pull the Docker image.
        """
        image_pull_policy = configuration._determine_image_pull_policy()

        if image_pull_policy is ImagePullPolicy.ALWAYS:
            return True
        elif image_pull_policy is ImagePullPolicy.NEVER:
            return False
        elif image_pull_policy is ImagePullPolicy.IF_NOT_PRESENT:
            try:
                # NOTE: images.get() wants the tag included with the image
                # name, while images.pull() wants them split.
                docker_client.images.get(configuration.image)
            except docker.errors.ImageNotFound:
                self._logger.debug(
                    f"Could not find Docker image locally: {configuration.image}"
                )
                return True
        return False

    def _pull_image(
        self, docker_client: "DockerClient", configuration: DockerWorkerJobConfiguration
    ):
        """
        Pull the image we're going to use to create the container.
        """
        image, tag = parse_image_tag(configuration.image)

        return docker_client.images.pull(image, tag)

    def _create_container(self, docker_client: "DockerClient", **kwargs) -> "Container":
        """
        Create a docker container with retries on name conflicts.

        If the container already exists with the given name, an incremented index is
        added.
        """
        # Create the container with retries on name conflicts (with an incremented idx)
        index = 0
        container = None
        name = original_name = kwargs.pop("name")

        while not container:
            from docker.errors import APIError

            try:
                display_name = repr(name) if name else "with auto-generated name"
                self._logger.info(f"Creating Docker container {display_name}...")
                container = docker_client.containers.create(name=name, **kwargs)
            except APIError as exc:
                if "Conflict" in str(exc) and "container name" in str(exc):
                    self._logger.info(
                        f"Docker container name {display_name} already exists; "
                        "retrying..."
                    )
                    index += 1
                    name = f"{original_name}-{index}"
                else:
                    raise

        self._logger.info(
            f"Docker container {container.name!r} has status {container.status!r}"
        )
        return container
