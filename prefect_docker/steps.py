"""
Core set of steps for specifying a Prefect project build step.
"""
import os
import sys
from pathlib import Path
from typing import Optional

import pendulum
from docker.models.images import Image
from prefect.docker import build_image, docker_client, get_prefect_image_name
from prefect.utilities.slugify import slugify


def build_docker_image(
    image_name: str,
    dockerfile: str = "Dockerfile",
    auto_build: bool = False,
    tag: Optional[str] = None,
    push: bool = True,
) -> dict:
    """
    Builds a Docker image for a Prefect deployment.

    Args:
        image_name: The name of the Docker image to build, including the registry and
            repository (e.g., "myregistry/myimage").
        dockerfile: The path to the Dockerfile used to build the image (default is
            "Dockerfile" in the current directory).
        auto_build: Whether to generate a Dockerfile automatically from the current
            directory (default is False).
        tag: The tag to apply to the built image (default is a slugified timestamp in
            UTC).
        push: Whether to push the built image to the registry (default is
            True).

    Returns:
        dict: A dictionary containing the image name and tag of the built image (e.g.,
            {"image_name": "myregistry/myimage:2023-03-30T12-34-56Z"}).
    """
    if auto_build:
        lines = []
        base_image = get_prefect_image_name()
        lines.append(f"FROM {base_image}")

        dir_name = os.path.basename(os.getcwd())
        lines.append(f"COPY . /opt/prefect/{dir_name}/")
        lines.append(f"WORKDIR /opt/prefect/{dir_name}/")

        if Path("requirements.txt").exists():
            lines.append("RUN pip install -r requirements.txt")

        if Path(dockerfile).exists():
            raise ValueError("Dockerfile already exists.")

        with Path(dockerfile).open("w") as f:
            f.writelines(line + "\n" for line in lines)

    try:
        image_id = build_image(
            context=Path("."),
            dockerfile=dockerfile,
            pull=True,
            stream_progress_to=sys.stdout,
        )
    finally:
        if auto_build and dockerfile is not None:
            os.unlink(dockerfile)

    if not tag:
        tag = slugify(pendulum.now("utc").isoformat())

    with docker_client() as client:
        image: Image = client.images.get(image_id)
        image.tag(image_name, tag=tag)

        if push:
            events = client.api.push(image_name, tag=tag, stream=True, decode=True)
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
                client.api.remove_image(f"{image_name}:{tag}", noprune=True)

    return dict(image_name=f"{image_name}:{tag}")