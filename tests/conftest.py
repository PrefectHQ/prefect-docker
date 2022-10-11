from unittest.mock import MagicMock

import pytest


@pytest.fixture
def mock_client():
    all_tags = [MagicMock(id="id_1"), MagicMock(id="id_2")]
    client = MagicMock(_authenticated=False)
    client.images.pull.side_effect = (
        lambda repository, **kwargs: all_tags if kwargs.get("all_tags") else all_tags[0]
    )
    return client


@pytest.fixture
def mock_docker(monkeypatch, mock_client) -> MagicMock:
    docker = MagicMock(DockerClient=mock_client)
    docker.from_env.side_effect = lambda **kwargs: mock_client
    monkeypatch.setattr("prefect_docker.host.docker", docker)
    return docker


@pytest.fixture
def mock_docker_host(mock_client):
    docker_host = MagicMock()
    docker_host.get_client.side_effect = lambda: mock_client
    return docker_host


@pytest.fixture
def mock_docker_registry_credentials():
    docker_registry_credentials = MagicMock()
    docker_registry_credentials.login.side_effect = lambda client: setattr(
        client, "_authenticated", True
    )
    return docker_registry_credentials
