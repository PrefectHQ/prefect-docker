from unittest.mock import MagicMock

import pytest

from prefect_docker.settings import DockerSettings


@pytest.fixture
def mock_docker(monkeypatch) -> MagicMock:
    docker = MagicMock(DockerClient=MagicMock())
    docker.from_env.side_effect = lambda **kwargs: kwargs
    monkeypatch.setattr("prefect_docker.settings.docker", docker)
    return docker


def test_docker_credentials_get_client(mock_docker: MagicMock):
    settings_kwargs = dict(
        base_url="unix:///var/run/docker.sock",
        version="1.35",
        max_pool_size=8,
        client_kwargs={"tls": True}
    )
    settings = DockerSettings(**settings_kwargs)
    for key, val in settings_kwargs.items():
        assert getattr(settings, key) == val

    settings.get_client()
    mock_docker.DockerClient.assert_called_once_with(
        base_url='unix:///var/run/docker.sock',
        version='1.35',
        timeout=None,
        max_pool_size=8,
        credstore_env={},
        tls=True
    )


def test_docker_credentials_get_client_from_env(mock_docker: MagicMock):
    settings_kwargs = dict(
        version="1.35",
        max_pool_size=8,
        client_kwargs={"assert_hostname": True}
    )
    settings = DockerSettings(**settings_kwargs)
    for key, val in settings_kwargs.items():
        assert getattr(settings, key) == val

    settings.get_client()
    mock_docker.from_env.assert_called_once_with(
        version='1.35',
        timeout=None,
        max_pool_size=8,
        credstore_env={},
        assert_hostname=True
    )
