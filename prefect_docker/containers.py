"""Integrations with Docker Containers."""

from typing import Any, Dict, List, Optional, Union

from prefect import task

from prefect_docker.host import DockerHost


@task
def create_docker_container(
    docker_host: DockerHost,
    image: str,
    command: Optional[Union[str, List[str]]] = None,
    name: Optional[str] = None,
    detach: Optional[bool] = None,
    **create_kwargs: Dict[str, Any]
) -> int:
    """
    Create a container without starting it. Similar to docker create.

    Args:
        docker_settings: Settings for interacting with a Docker host.
        image: The image to run.
        command: The command(s) to run in the container.
        name: The name for this container.
        detach: Run container in the background.
        create_kwargs: Additional keyword arguments to pass to
            [`client.containers.create`](https://docker-py.readthedocs.io/en/stable/containers.html#docker.models.containers.ContainerCollection.create).

    Returns:
        A Container's ID.

    Examples:
        Create a container with the Prefect image.
        ```
        from prefect import flow
        from prefect_docker import DockerSettings
        from prefect_docker.containers import create_docker_container

        @flow
        def create_docker_container_flow():
            docker_settings = DockerSettings()
            container = create_docker_container(
                docker_settings=docker_settings,
                image="prefecthq/prefect",
                command="echo 'hello world!'"
            )

        create_docker_container_flow()
        ```
    """
    client = docker_host.get_client()
    container = client.containers.create(
        image=image, command=command, name=name, detach=detach, **create_kwargs
    )
    return container.id
