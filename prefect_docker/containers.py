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


@task
async def get_docker_container_logs(
    container_id: str,
    docker_host: Optional[DockerHost] = None,
    **logs_kwargs: Dict[str, Any],
) -> str:
    """
    Get logs from this container. Similar to the docker logs command.

    Args:
        container_id: The container ID to pull logs from.
        docker_host: Settings for interacting with a Docker host.
        **logs_kwargs: Additional keyword arguments to pass to
            [`client.containers.get(container_id).logs`](https://docker-py.readthedocs.io/en/stable/containers.html#docker.models.containers.Container.logs).

    Returns:
        The Container's logs.

    Examples:
        Gets logs from a container with an ID that starts with "c157".
        ```
        from prefect import flow
        from prefect_docker.containers import get_docker_container_logs

        @flow
        def get_docker_container_logs_flow():
            logs = get_docker_container_logs(container_id="c157")
            return logs

        get_docker_container_logs_flow()
        ```

    """
    logger = get_run_logger()

    with (docker_host or DockerHost()).get_client() as client:
        logger.info(f"Retrieving logs from {container_id!r} container.")
        container = await run_sync_in_worker_thread(client.containers.get, container_id)
        logs = await run_sync_in_worker_thread(container.logs, **logs_kwargs)

    return logs.decode()


@task
async def start_docker_container(
    container_id: str,
    docker_host: Optional[DockerHost] = None,
    **start_kwargs: Dict[str, Any],
) -> Container:
    """
    Start this container. Similar to the docker start command.

    Args:
        container_id: The container ID to start.
        docker_host: Settings for interacting with a Docker host.
        **start_kwargs: Additional keyword arguments to pass to
            [`client.containers.get(container_id).start`](https://docker-py.readthedocs.io/en/stable/containers.html#docker.models.containers.Container.start).

    Returns:
        The Docker Container object.

    Examples:
        Start a container with an ID that starts wtih "c157".
        ```
        from prefect import flow
        from prefect_docker.containers import start_docker_container

        @flow
        def start_docker_container_flow():
            container_id = start_docker_container(container_id="c157")
            return container_id

        start_docker_container_flow()
        ```
    """
    logger = get_run_logger()

    with (docker_host or DockerHost()).get_client() as client:
        logger.info(f"Starting {container_id!r} container.")
        container = await run_sync_in_worker_thread(client.containers.get, container_id)
        await run_sync_in_worker_thread(container.start, **start_kwargs)

    return container