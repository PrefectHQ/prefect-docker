from unittest.mock import MagicMock

from prefect_docker.containers import create_docker_container


def test_create_docker_container(mock_docker_settings: MagicMock):
    create_kwargs = dict(
        image="test_image",
        command="test_command",
        name="test_name",
        detach=False,
        ports={"2222/tcp": 3333},
    )
    create_docker_container.fn(mock_docker_settings, **create_kwargs)
    client = mock_docker_settings.get_client()
    client.containers.create.assert_called_once_with(**create_kwargs)
