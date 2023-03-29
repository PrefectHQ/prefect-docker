"""Module containing docker credentials."""
import docker
from prefect import get_run_logger
from prefect.blocks.core import Block
from prefect.utilities.asyncutils import run_sync_in_worker_thread
from pydantic import Field, SecretStr


class DockerRegistryCredentials(Block):
    """
    Block used to manage credentials for interacting with a Docker Registry.

    Examples:
        Log into Docker Registry.
        ```python
        from prefect_docker import DockerHost, DockerRegistryCredentials

        docker_host = DockerHost()
        docker_registry_credentials = DockerRegistryCredentials(
            username="my_username",
            password="my_password",
            registry_url="registry.hub.docker.com",
        )
        with docker_host.get_client() as client:
            docker_registry_credentials.login(client)
        ```
    """

    _block_type_name = "Docker Registry Credentials"
    _logo_url = "https://images.ctfassets.net/gm98wzqotmnx/2IfXXfMq66mrzJBDFFCHTp/6d8f320d9e4fc4393f045673d61ab612/Moby-logo.png?h=250"  # noqa
    _description = "Store credentials for interacting with a Docker Registry."

    username: str = Field(
        default=..., description="The username to log into the registry with."
    )
    password: SecretStr = Field(
        default=..., description="The password to log into the registry with."
    )
    registry_url: str = Field(
        default=...,
        description=(
            'The URL to the registry. Generally, "http" or "https" can be omitted.'
        ),
        example="registry.hub.docker.com",
    )
    reauth: bool = Field(
        default=True,
        description="Whether or not to reauthenticate on each interaction.",
    )

    async def login(self, client: docker.DockerClient):
        """
        Authenticates a given Docker client with the configured Docker registry.

        Args:
            client: A Docker Client.
        """
        logger = get_run_logger()
        logger.debug(f"Logging into {self.registry_url}.")
        await run_sync_in_worker_thread(
            client.login,
            username=self.username,
            password=self.password.get_secret_value(),
            registry=self.registry_url,
            # See https://github.com/docker/docker-py/issues/2256 for information on
            # the default value for reauth.
            reauth=self.reauth,
        )
