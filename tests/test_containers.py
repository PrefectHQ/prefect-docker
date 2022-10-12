from unittest.mock import MagicMock

from prefect.logging import disable_run_logger

from prefect_docker.containers import create_docker_container, get_docker_container_logs


def test_create_docker_container(mock_docker_host: MagicMock):
    create_kwargs = dict(
        image="test_image",
        command="test_command",
        name="test_name",
        detach=False,
        ports={"2222/tcp": 3333},
    )
    with disable_run_logger():
        create_docker_container.fn(docker_host=mock_docker_host, **create_kwargs)
    client = mock_docker_host.get_client()
    client.containers.create.assert_called_once_with(**create_kwargs)


def test_get_docker_container_logs(mock_docker_host: MagicMock):
    with disable_run_logger():
        get_docker_container_logs.fn(container_id="m42", docker_host=mock_docker_host)
    client = mock_docker_host.get_client()
    client.containers.get.assert_called_once_with("m42")

    container = client.containers.get()
    container.logs.assert_called_once()
