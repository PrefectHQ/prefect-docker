"""
Prefect project steps for building and pushing Docker images.
"""
import os
import sys
from pathlib import Path
from typing import Dict, Optional

import pendulum
from docker.models.images import Image
from prefect.docker import build_image, docker_client, get_prefect_image_name
from prefect.utilities.slugify import slugify
from typing_extensions import TypedDict


class BuildDockerImageResult(TypedDict):
    """
    The result of a `build_docker_image` step.

    Attributes:
        image_name: The name and tag of the built image.
        image_tag: The tag of the built image.
    """

    image_name: str
    image_tag: str


def build_docker_image(
    image_name: str,
    dockerfile: str = "Dockerfile",
    tag: Optional[str] = None,
    push: bool = True,
    credentials: Optional[Dict] = None,
) -> BuildDockerImageResult:
    """
    Builds a Docker image for a Prefect deployment.

    Can be used within the `prefect.yaml` file of a Prefect project to build a Docker
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

    Returns:
        A dictionary containing the image name and tag of the
            built image.

    Examples:
        Build and push a Docker image prior to creating a deployment:
        ```yaml
        build:
            - prefect_docker.projects.steps.build_docker_image:
                requires: prefect-docker
                image_name: repo-name/image-name
                tag: dev
        ```

        Build a Docker image without pushing it to the registry:
        ```yaml
        build:
            - prefect_docker.projects.steps.build_docker_image:
                requires: prefect-docker
                image_name: repo-name/image-name
                tag: dev
                push: false
        ```

        Build a Docker image using a temporary Dockerfile:
        ```yaml
        build:
            - prefect_docker.projects.steps.build_docker_image:
                requires: prefect-docker
                image_name: repo-name/image-name
                tag: dev
                dockerfile: auto
        ```

        Build a Docker image using a temporary Dockerfile and push it to a private
        registry:
        ```yaml
        build:
            - prefect_docker.projects.steps.build_docker_image:
                requires: prefect-docker
                image_name: repo-name/image-name
                tag: dev
                dockerfile: auto
                credentials: "{{ prefect.block.docker-registry-credentials.dev-registry }}"
        ```
    """  # noqa
    auto_build = dockerfile == "auto"
    if auto_build:
        lines = []
        base_image = get_prefect_image_name()
        lines.append(f"FROM {base_image}")

        dir_name = os.path.basename(os.getcwd())
        lines.append(f"COPY . /opt/prefect/{dir_name}/")
        lines.append(f"WORKDIR /opt/prefect/{dir_name}/")

        if Path("requirements.txt").exists():
            lines.append("RUN python -m pip install -r requirements.txt")

        temp_dockerfile = Path("Dockerfile")
        if Path(temp_dockerfile).exists():
            raise ValueError("Dockerfile already exists.")

        with Path(temp_dockerfile).open("w") as f:
            f.writelines(line + "\n" for line in lines)

        dockerfile = str(temp_dockerfile)

    try:
        image_id = build_image(
            context=Path("."),
            dockerfile=dockerfile,
            pull=True,
            stream_progress_to=sys.stdout,
        )
    finally:
        if auto_build:
            os.unlink(dockerfile)

    if not tag:
        tag = slugify(pendulum.now("utc").isoformat())

    with docker_client() as client:
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

    return {"image_name": f"{image_name}:{tag}", "image_tag": tag}
