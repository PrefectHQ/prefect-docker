from pathlib import Path
from unittest import mock
from unittest.mock import MagicMock

import docker
import docker.models.containers
import docker.models.images
import pendulum
import prefect
import prefect.docker
import pytest

from prefect_docker.projects.steps import build_docker_image

FAKE_CONTAINER_ID = "fake-id"
FAKE_BASE_URL = "http+docker://my-url"
FAKE_DEFAULT_TAG = "2022-08-31t18-01-32-00-00"


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
    fake_api.base_url = FAKE_BASE_URL
    mock_client.api = fake_api

    mock_docker_client_func = MagicMock(
        name="docker_client", spec=prefect.docker.docker_client
    )
    mock_docker_client_func.return_value.__enter__.return_value = mock_client
    monkeypatch.setattr(
        "prefect_docker.projects.steps.docker_client", mock_docker_client_func
    )
    return mock_client


@pytest.fixture
def mock_build_image(monkeypatch):
    mock_build_image = MagicMock(name="build_image", spec=prefect.docker.build_image)
    mock_build_image.return_value = FAKE_CONTAINER_ID
    monkeypatch.setattr("prefect_docker.projects.steps.build_image", mock_build_image)
    return mock_build_image


@pytest.fixture
def mock_pendulum(monkeypatch):
    mock_pendulum = MagicMock(name="pendulum", spec=pendulum)
    mock_pendulum.now.return_value = pendulum.datetime(2022, 8, 31, 18, 1, 32)
    monkeypatch.setattr("prefect_docker.projects.steps.pendulum", mock_pendulum)
    return mock_pendulum


@pytest.mark.parametrize(
    "kwargs, expected_image_name",
    [
        ({"image_name": "registry/repo"}, f"registry/repo:{FAKE_DEFAULT_TAG}"),
        (
            {"image_name": "registry/repo", "dockerfile": "Dockerfile.dev"},
            f"registry/repo:{FAKE_DEFAULT_TAG}",
        ),
        (
            {"image_name": "registry/repo", "tag": "mytag"},
            "registry/repo:mytag",
        ),
        (
            {"image_name": "registry/repo", "push": False},
            f"registry/repo:{FAKE_DEFAULT_TAG}",
        ),
        (
            {"image_name": "registry/repo", "dockerfile": "auto"},
            f"registry/repo:{FAKE_DEFAULT_TAG}",
        ),
    ],
)
def test_build_docker_image(
    monkeypatch,
    mock_docker_client,
    mock_build_image,
    mock_pendulum,
    kwargs,
    expected_image_name,
):
    auto_build = False
    image_name = kwargs.get("image_name")
    dockerfile = kwargs.get("dockerfile", "Dockerfile")
    tag = kwargs.get("tag", FAKE_DEFAULT_TAG)
    push = kwargs.get("push", True)
    result = build_docker_image(**kwargs)

    assert result["image_name"] == expected_image_name

    if dockerfile == "auto":
        auto_build = True
        dockerfile = "Dockerfile"

    mock_build_image.assert_called_once_with(
        context=Path("."),
        dockerfile=dockerfile,
        pull=True,
        stream_progress_to=mock.ANY,
    )
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
            image=expected_image_name, noprune=True
        )
    else:
        mock_docker_client.api.push.assert_not_called()

    if auto_build:
        assert not Path("Dockerfile").exists()


def test_build_docker_image_raises_with_auto_and_existing_dockerfile():
    try:
        Path("Dockerfile").touch()
        with pytest.raises(ValueError, match="Dockerfile already exists"):
            build_docker_image(image_name="registry/repo", dockerfile="auto")
    finally:
        Path("Dockerfile").unlink()


def test_real_auto_dockerfile_build(docker_client_with_cleanup):
    try:
        result = build_docker_image(
            image_name="local/repo", tag="test", dockerfile="auto", push=False
        )
        image: docker.models.images.Image = docker_client_with_cleanup.images.get(
            result["image_name"]
        )
        assert image

        cases = [
            {"command": "prefect version", "expected": prefect.__version__},
            {"command": "ls", "expected": "requirements.txt"},
            {
                "command": "python -c 'import docker; print(docker.__version__)'",
                "expected": docker.__version__,
            },
        ]

        for case in cases:
            output = docker_client_with_cleanup.containers.run(
                image=result["image_name"],
                command=case["command"],
                labels=["prefect-docker-test"],
                remove=True,
            )
            assert case["expected"] in output.decode()

    finally:
        docker_client_with_cleanup.containers.prune(
            filters={"label": "prefect-docker-test"}
        )
        image = docker_client_with_cleanup.images.get("local/repo:test")
        if image:
            docker_client_with_cleanup.images.remove(
                image="local/repo:test", force=True
            )
