"""Integrations with Docker Containers."""

from typing import Any, Dict, List, Optional, Union

from docker.models.containers import Container
from prefect import task

from prefect_docker.settings import DockerSettings


@task
def create_docker_container(
    docker_settings: DockerSettings,
    image: str,
    command: Optional[Union[str, List[str]]] = None,
    name: Optional[str] = None,
    **create_kwargs: Dict[str, Any]
) -> Container:
    """
    Create a container without starting it. Similar to docker create.

    Args:
        docker_settings: Settings for interacting with a Docker host.
        image: The image to run.
        command: The command(s) to run in the container.
        name: The name for this container.
        create_kwargs: Additional keyword arguments to pass to
            [`client.containers.create`](https://docker-py.readthedocs.io/en/stable/containers.html#docker.models.containers.ContainerCollection.create).

    Returns:
        A Container object.
    """
    client = docker_settings.get_client()
    container = client.containers.create(
        image=image, command=command, name=name, **create_kwargs
    )
    return container
