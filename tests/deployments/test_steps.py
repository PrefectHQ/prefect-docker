import sys
from pathlib import Path
from unittest.mock import MagicMock

import docker
import docker.errors
import docker.models.containers
import docker.models.images
import pendulum
import prefect
import prefect.utilities.dockerutils
import pytest

from prefect_docker.deployments.steps import build_docker_image, push_docker_image

FAKE_CONTAINER_ID = "fake-id"
FAKE_BASE_URL = "http+docker://my-url"
FAKE_DEFAULT_TAG = "2022-08-31t18-01-32-00-00"
FAKE_IMAGE_NAME = "registry/repo"
FAKE_TAG = "mytag"
FAKE_EVENT = [{"status": "status", "progress": "progress"}, {"status": "status"}]
FAKE_CREDENTIALS = {
    "username": "user",
    "password": "pass",
    "registry_url": "https://registry.com",
    "reauth": True,
}


@pytest.fixture
def mock_docker_client(monkeypatch):
    mock_client = MagicMock(name="DockerClient", spec=docker.DockerClient)
    mock_client.version.return_value = {"Version": "20.10"}

    # Build a fake container object to return
    fake_container = docker.models.containers.Container()
    fake_container.client = MagicMock(name="Container.client")
    fake_container.collection = MagicMock(name="Container.collection")
    attrs = {
        "Id": FAKE_CONTAINER_ID,
        "Name": "fake-name",
        "State": {
            "Status": "exited",
            "Running": False,
            "Paused": False,
            "Restarting": False,
            "OOMKilled": False,
            "Dead": True,
            "Pid": 0,
            "ExitCode": 0,
            "Error": "",
            "StartedAt": "2022-08-31T18:01:32.645851548Z",
            "FinishedAt": "2022-08-31T18:01:32.657076632Z",
        },
    }
    fake_container.collection.get().attrs = attrs
    fake_container.attrs = attrs
    fake_container.stop = MagicMock()
    # Return the fake container on lookups and creation
    mock_client.containers.get.return_value = fake_container
    mock_client.containers.create.return_value = fake_container

    # Set attributes for infrastructure PID lookup
    fake_api = MagicMock(name="APIClient")
    fake_api.build.return_value = [
        {"aux": {"ID": FAKE_CONTAINER_ID}},
    ]
    fake_api.base_url = FAKE_BASE_URL
    mock_client.api = fake_api

    mock_docker_client_func = MagicMock(
        name="docker_client", spec=prefect.utilities.dockerutils.docker_client
    )
    mock_docker_client_func.return_value.__enter__.return_value = mock_client
    monkeypatch.setattr(
        "prefect_docker.deployments.steps.docker_client", mock_docker_client_func
    )
    return mock_client


@pytest.fixture
def mock_pendulum(monkeypatch):
    mock_pendulum = MagicMock(name="pendulum", spec=pendulum)
    mock_pendulum.now.return_value = pendulum.datetime(2022, 8, 31, 18, 1, 32)
    monkeypatch.setattr("prefect_docker.deployments.steps.pendulum", mock_pendulum)
    return mock_pendulum


@pytest.mark.parametrize(
    "kwargs, expected_image",
    [
        ({"image_name": "registry/repo"}, f"registry/repo:{FAKE_DEFAULT_TAG}"),
        (
            {
                "image_name": "registry/repo",
                "dockerfile": "Dockerfile.dev",
                "push": True,
            },
            f"registry/repo:{FAKE_DEFAULT_TAG}",
        ),
        (
            {"image_name": "registry/repo", "tag": "mytag", "push": True},
            "registry/repo:mytag",
        ),
        (
            {
                "image_name": "registry/repo",
            },
            f"registry/repo:{FAKE_DEFAULT_TAG}",
        ),
        (
            {"image_name": "registry/repo", "dockerfile": "auto"},
            f"registry/repo:{FAKE_DEFAULT_TAG}",
        ),
        (
            {
                "image_name": "registry/repo",
                "dockerfile": "auto",
                "push": True,
                "credentials": {
                    "username": "user",
                    "password": "pass",
                    "registry_url": "https://registry.com",
                    "reauth": True,
                },
            },
            f"registry/repo:{FAKE_DEFAULT_TAG}",
        ),
    ],
)
def test_build_docker_image(
    monkeypatch,
    mock_docker_client,
    mock_pendulum,
    kwargs,
    expected_image,
):
    auto_build = False
    image_name = kwargs.get("image_name")
    dockerfile = kwargs.get("dockerfile", "Dockerfile")
    tag = kwargs.get("tag", FAKE_DEFAULT_TAG)
    push = kwargs.get("push", False)
    credentials = kwargs.get("credentials", None)
    result = build_docker_image(**kwargs)

    assert result["image"] == expected_image
    assert result["tag"] == tag
    assert result["image_name"] == image_name
    assert result["image_id"] == FAKE_CONTAINER_ID

    if dockerfile == "auto":
        auto_build = True
        dockerfile = "Dockerfile"

    mock_docker_client.images.get.assert_called_once_with(FAKE_CONTAINER_ID)
    mock_docker_client.images.get.return_value.tag.assert_called_once_with(
        repository=image_name, tag=tag
    )
    if push:
        mock_docker_client.api.push.assert_called_once_with(
            repository=image_name,
            tag=tag,
            stream=True,
            decode=True,
        )
        mock_docker_client.api.remove_image.assert_called_once_with(
            image=expected_image, noprune=True
        )
    else:
        mock_docker_client.api.push.assert_not_called()

    if auto_build:
        assert not Path("Dockerfile").exists()

    if credentials:
        mock_docker_client.login.assert_called_once_with(
            username=credentials["username"],
            password=credentials["password"],
            registry=credentials["registry_url"],
            reauth=credentials.get("reauth", True),
        )
    else:
        mock_docker_client.login.assert_not_called()


def test_build_docker_image_raises_with_auto_and_existing_dockerfile():
    try:
        Path("Dockerfile").touch()
        with pytest.raises(ValueError, match="Dockerfile already exists"):
            build_docker_image(image_name="registry/repo", dockerfile="auto")
    finally:
        Path("Dockerfile").unlink()


def test_push_docker_image_with_credentials(mock_docker_client, monkeypatch):
    # Mock stdout
    mock_stdout = MagicMock()
    monkeypatch.setattr(sys, "stdout", mock_stdout)

    mock_docker_client.api.push.return_value = FAKE_EVENT

    result = push_docker_image(
        image_name=FAKE_IMAGE_NAME, tag=FAKE_TAG, credentials=FAKE_CREDENTIALS
    )

    assert result["image_name"] == FAKE_IMAGE_NAME
    assert result["tag"] == FAKE_TAG
    assert result["image"] == f"{FAKE_IMAGE_NAME}:{FAKE_TAG}"

    mock_docker_client.login.assert_called_once_with(
        username=FAKE_CREDENTIALS["username"],
        password=FAKE_CREDENTIALS["password"],
        registry=FAKE_CREDENTIALS["registry_url"],
        reauth=FAKE_CREDENTIALS.get("reauth", True),
    )
    mock_docker_client.api.push.assert_called_once_with(
        repository=FAKE_IMAGE_NAME,
        tag=FAKE_TAG,
        stream=True,
        decode=True,
    )
    assert mock_stdout.write.call_count == 5


def test_push_docker_image_without_credentials(mock_docker_client, monkeypatch):
    # Mock stdout
    mock_stdout = MagicMock()
    monkeypatch.setattr(sys, "stdout", mock_stdout)

    mock_docker_client.api.push.return_value = FAKE_EVENT

    result = push_docker_image(
        image_name=FAKE_IMAGE_NAME,
        tag=FAKE_TAG,
    )

    assert result["image_name"] == FAKE_IMAGE_NAME
    assert result["tag"] == FAKE_TAG
    assert result["image"] == f"{FAKE_IMAGE_NAME}:{FAKE_TAG}"

    mock_docker_client.login.assert_not_called()
    mock_docker_client.api.push.assert_called_once_with(
        repository=FAKE_IMAGE_NAME,
        tag=FAKE_TAG,
        stream=True,
        decode=True,
    )
    assert mock_stdout.write.call_count == 5


def test_push_docker_image_raises_on_event_error(mock_docker_client):
    error_event = [{"error": "Error"}]
    mock_docker_client.api.push.return_value = error_event

    with pytest.raises(OSError, match="Error"):
        push_docker_image(
            image_name=FAKE_IMAGE_NAME, tag=FAKE_TAG, credentials=FAKE_CREDENTIALS
        )
