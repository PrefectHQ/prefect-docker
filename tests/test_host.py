from unittest.mock import MagicMock

import pytest

from prefect_docker.host import DockerHost


@pytest.fixture
def mock_docker(monkeypatch) -> MagicMock:
    docker = MagicMock(DockerClient=MagicMock())
    docker.from_env.side_effect = lambda **kwargs: kwargs
    monkeypatch.setattr("prefect_docker.host.docker", docker)
    return docker


def test_docker_host_get_client(mock_docker: MagicMock):
    settings_kwargs = dict(
        base_url="unix:///var/run/docker.sock",
        version="1.35",
        max_pool_size=8,
        client_kwargs={"tls": True},
        credstore_env=None,
    )
    settings = DockerHost(**settings_kwargs)
    for key, val in settings_kwargs.items():
        assert getattr(settings, key) == val

    settings.get_client()
    mock_docker.DockerClient.assert_called_once_with(
        base_url="unix:///var/run/docker.sock",
        version="1.35",
        timeout=None,
        max_pool_size=8,
        tls=True,
    )


def test_docker_host_get_client_from_env(mock_docker: MagicMock):
    settings_kwargs = dict(
        version="1.35",
        max_pool_size=8,
        client_kwargs={"assert_hostname": True},
        credstore_env=None,
    )
    settings = DockerHost(**settings_kwargs)
    for key, val in settings_kwargs.items():
        assert getattr(settings, key) == val

    settings.get_client()
    mock_docker.from_env.assert_called_once_with(
        version="1.35",
        timeout=None,
        max_pool_size=8,
        assert_hostname=True,
    )
