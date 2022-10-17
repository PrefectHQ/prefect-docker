"""Integrations with Docker Containers."""

from typing import Any, Container, Dict, List, Optional, Union

from prefect import get_run_logger, task
from prefect.utilities.asyncutils import run_sync_in_worker_thread

from prefect_docker.host import DockerHost


@task
async def create_docker_container(
    image: str,
    command: Optional[Union[str, List[str]]] = None,
    name: Optional[str] = None,
    detach: Optional[bool] = None,
    docker_host: Optional[DockerHost] = None,
    **create_kwargs: Dict[str, Any],
) -> Container:
    """
    Create a container without starting it. Similar to docker create.

    Args:
        image: The image to run.
        command: The command(s) to run in the container.
        name: The name for this container.
        detach: Run container in the background.
        docker_host: Settings for interacting with a Docker host.
        **create_kwargs: Additional keyword arguments to pass to
            [`client.containers.create`](https://docker-py.readthedocs.io/en/stable/containers.html#docker.models.containers.ContainerCollection.create).

    Returns:
        A Docker Container object.

    Examples:
        Create a container with the Prefect image.
        ```
        from prefect import flow
        from prefect_docker.containers import create_docker_container

        @flow
        def create_docker_container_flow():
            container = create_docker_container(
                image="prefecthq/prefect",
                command="echo 'hello world!'"
            )

        create_docker_container_flow()
        ```
    """
    logger = get_run_logger()

    with (docker_host or DockerHost()).get_client() as client:
        logger.info(f"Creating container with {image!r} image.")
        container = await run_sync_in_worker_thread(
            client.containers.create,
            image=image,
            command=command,
            name=name,
            detach=detach,
            **create_kwargs,
        )
    return container
