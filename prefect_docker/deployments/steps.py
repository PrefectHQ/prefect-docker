"""
Prefect deployment steps for building and pushing Docker images.


These steps can be used in a `prefect.yaml` file to define the default
build steps for a group of deployments, or they can be used to define
the build step for a specific deployment.

!!! example
    Build a Docker image before deploying a flow:
    ```yaml
    build:
        - prefect_docker.deployments.steps.build_docker_image:
            requires: prefect-docker
            image_name: repo-name/image-name
            tag: dev
    ```
"""
import os
import sys
from pathlib import Path
from typing import Dict, Optional

import docker.errors
import pendulum
from docker.models.images import Image
from prefect.utilities.dockerutils import (
    IMAGE_LABELS,
    BuildError,
    docker_client,
    get_prefect_image_name,
)
from prefect.utilities.slugify import slugify
from typing_extensions import TypedDict


class BuildDockerImageResult(TypedDict):
    """
    The result of a `build_docker_image` step.

    Attributes:
        image_name: The name of the built image.
        image_tag: The tag of the built image.
        image: The name and tag of the built image.
        image_id: The ID of the built image.
    """

    image_name: str
    image_tag: str
    image: str
    image_id: str


def build_docker_image(
    image_name: str,
    dockerfile: str = "Dockerfile",
    tag: Optional[str] = None,
    push: bool = False,
    credentials: Optional[Dict] = None,
    **build_kwargs,
) -> BuildDockerImageResult:
    """
    Builds a Docker image for a Prefect deployment.

    Can be used within a `prefect.yaml` file to build a Docker
    image prior to creating or updating a deployment.

    Args:
        image_name: The name of the Docker image to build, including the registry and
            repository.
        dockerfile: The path to the Dockerfile used to build the image. If "auto" is
            passed, a temporary Dockerfile will be created to build the image.
        tag: The tag to apply to the built image.
        push: Whether to push the built image to the registry.
        credentials: A dictionary containing the username, password, and URL for the
            registry to push the image to.
        **build_kwargs: Additional keyword arguments to pass to Docker when building
            the image. Available options can be found in the [`docker-py`](https://docker-py.readthedocs.io/en/stable/images.html#docker.models.images.ImageCollection.build)
            documentation.

    Returns:
        A dictionary containing the image name and tag of the
            built image.

    Example:
        Build and push a Docker image prior to creating a deployment:
        ```yaml
        build:
            - prefect_docker.deployments.steps.build_docker_image:
                requires: prefect-docker
                image_name: repo-name/image-name
                tag: dev
                push: true
        ```

        Build a Docker image without pushing it to a remote registry:
        ```yaml
        build:
            - prefect_docker.deployments.steps.build_docker_image:
                requires: prefect-docker
                image_name: repo-name/image-name
                tag: dev
                push: false
        ```

        Build a Docker image using an auto-generated Dockerfile:
        ```yaml
        build:
            - prefect_docker.deployments.steps.build_docker_image:
                requires: prefect-docker
                image_name: repo-name/image-name
                tag: dev
                dockerfile: auto
                push: false
        ```

        Build a Docker image using an auto-generated Dockerfile and push it to a private
        registry:
        ```yaml
        build:
            - prefect_docker.deployments.steps.build_docker_image:
                requires: prefect-docker
                image_name: repo-name/image-name
                tag: dev
                dockerfile: auto
                push: false
                credentials: "{{ prefect.blocks.docker-registry-credentials.dev-registry }}"
        ```

        Build a Docker image for a different platform:
        ```yaml
        build:
            - prefect_docker.deployments.steps.build_docker_image:
                requires: prefect-docker
                image_name: repo-name/image-name
                tag: dev
                dockerfile: Dockerfile
                push: false
                platform: amd64
        ```
    """  # noqa
    auto_build = dockerfile == "auto"
    if auto_build:
        lines = []
        base_image = get_prefect_image_name()
        lines.append(f"FROM {base_image}")
        dir_name = os.path.basename(os.getcwd())

        if Path("requirements.txt").exists():
            lines.append(
                f"COPY requirements.txt /opt/prefect/{dir_name}/requirements.txt"
            )
            lines.append("RUN python -m pip install -r requirements.txt")

        lines.append(f"COPY . /opt/prefect/{dir_name}/")
        lines.append(f"WORKDIR /opt/prefect/{dir_name}/")

        temp_dockerfile = Path("Dockerfile")
        if Path(temp_dockerfile).exists():
            raise ValueError("Dockerfile already exists.")

        with Path(temp_dockerfile).open("w") as f:
            f.writelines(line + "\n" for line in lines)

        dockerfile = str(temp_dockerfile)

    build_kwargs["path"] = os.getcwd()
    build_kwargs["dockerfile"] = dockerfile
    build_kwargs["pull"] = build_kwargs.get("pull", True)
    build_kwargs["decode"] = True
    build_kwargs["labels"] = {**build_kwargs.get("labels", {}), **IMAGE_LABELS}
    image_id = None

    with docker_client() as client:
        try:
            events = client.api.build(**build_kwargs)

            try:
                for event in events:
                    if "stream" in event:
                        sys.stdout.write(event["stream"])
                        sys.stdout.flush()
                    elif "aux" in event:
                        image_id = event["aux"]["ID"]
                    elif "error" in event:
                        raise BuildError(event["error"])
                    elif "message" in event:
                        raise BuildError(event["message"])
            except docker.errors.APIError as e:
                raise BuildError(e.explanation) from e

        finally:
            if auto_build:
                os.unlink(dockerfile)

        if not isinstance(image_id, str):
            raise BuildError("Docker did not return an image ID for built image.")

        if not tag:
            tag = slugify(pendulum.now("utc").isoformat())

        if credentials is not None:
            client.login(
                username=credentials.get("username"),
                password=credentials.get("password"),
                registry=credentials.get("registry_url"),
                reauth=credentials.get("reauth", True),
            )
        image: Image = client.images.get(image_id)
        image.tag(repository=image_name, tag=tag)

        if push:
            events = client.api.push(
                repository=image_name, tag=tag, stream=True, decode=True
            )
            try:
                for event in events:
                    if "status" in event:
                        sys.stdout.write(event["status"])
                        if "progress" in event:
                            sys.stdout.write(" " + event["progress"])
                        sys.stdout.write("\n")
                        sys.stdout.flush()
                    elif "error" in event:
                        raise OSError(event["error"])
            finally:
                client.api.remove_image(image=f"{image_name}:{tag}", noprune=True)

    return {
        "image_name": image_name,
        "image_tag": tag,
        "image": f"{image_name}:{tag}",
        "image_id": image_id,
    }
