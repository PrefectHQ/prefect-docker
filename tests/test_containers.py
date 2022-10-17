from unittest.mock import MagicMock

from prefect.logging import disable_run_logger

from prefect_docker.containers import (
    create_docker_container,
    get_docker_container_logs,
    start_docker_container,
)


class TestCreateDockerContainer:
    async def test_create_kwargs(self, mock_docker_host: MagicMock):
        create_kwargs = dict(
            image="test_image",
            command="test_command",
            name="test_name",
            detach=False,
            ports={"2222/tcp": 3333},
        )
        with disable_run_logger():
            container_id = await create_docker_container.fn(
                docker_host=mock_docker_host, **create_kwargs
            )
        assert container_id == "id_1"

        client = mock_docker_host.get_client()
        client.__enter__.return_value.containers.create.assert_called_once_with(
            **create_kwargs
        )


class TestGetDockerContainerLogs:
    async def test_logs_kwargs(self, mock_docker_host: MagicMock):
        logs_kwargs = dict(container_id=42)
        with disable_run_logger():
            logs = await get_docker_container_logs.fn(
                docker_host=mock_docker_host, **logs_kwargs
            )
        assert logs == "here are logs"


class TestStartDockerContainer:
    async def test_start_kwargs(self, mock_docker_host: MagicMock):
        start_kwargs = dict(container_id=42)
        with disable_run_logger():
            logs = await start_docker_container.fn(
                docker_host=mock_docker_host, **start_kwargs
            )
        assert logs == "here are logs"
