from unittest.mock import MagicMock, patch

import docker
import pytest


def mock_images_pull(all_tags=False, **kwargs):
    tags_list = [MagicMock(id="id_1"), MagicMock(id="id_2")]
    return tags_list if all_tags else tags_list[0]


@pytest.fixture
def mock_docker_container():
    container = MagicMock()
    container.logs.side_effect = lambda **logs_kwargs: b"here are logs"
    return container


@pytest.fixture
def mock_docker_client(mock_docker_container):
    client = MagicMock(_authenticated=False)
    client.return_value.__enter__.return_value.images.pull.side_effect = (
        mock_images_pull
    )
    client.__enter__.return_value.images.pull.side_effect = mock_images_pull
    client.__enter__.return_value.containers.create.return_value = MagicMock(id="id_1")
    client.__enter__.return_value.containers.get.return_value = mock_docker_container
    return client


@pytest.fixture
def mock_docker_client_new(mock_docker_client) -> MagicMock:
    with patch.object(
        docker.DockerClient, "__new__", mock_docker_client
    ) as magic_docker_client:
        yield magic_docker_client


@pytest.fixture
def mock_docker_client_from_env(mock_docker_client) -> MagicMock:
    with patch.object(
        docker.DockerClient, "from_env", mock_docker_client
    ) as magic_docker_client:
        yield magic_docker_client


@pytest.fixture
def mock_docker_host(mock_docker_client):
    docker_host = MagicMock()
    docker_host.get_client.side_effect = lambda: mock_docker_client
    return docker_host


async def mock_login(client):
    client._authenticated = True


@pytest.fixture
def mock_docker_registry_credentials():
    docker_registry_credentials = MagicMock()
    docker_registry_credentials.login.side_effect = mock_login
    return docker_registry_credentials
