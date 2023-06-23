import os
import sys
import uuid
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

import docker
import docker.errors
import docker.models.containers
import docker.models.images
import prefect
import prefect.utilities.dockerutils
import pytest
from docker import DockerClient
from docker.errors import APIError
from docker.models.containers import Container
from prefect.client.schemas import FlowRun
from prefect.utilities.dockerutils import IMAGE_LABELS, get_prefect_image_name

from prefect_docker.deployments.steps import build_docker_image
from prefect_docker.worker import (
    CONTAINER_LABELS,
    DockerWorker,
    DockerWorkerJobConfiguration,
)

CLIENT = docker.from_env()


@pytest.fixture
def default_docker_worker_job_configuration():
    return DockerWorkerJobConfiguration()


@pytest.fixture
def flow_run():
    return FlowRun(flow_id=uuid.uuid4())


@pytest.fixture(autouse=True)
def bypass_api_check(monkeypatch):
    monkeypatch.setenv("PREFECT_DOCKER_TEST_MODE", True)


@pytest.fixture(scope="session")
def docker_client_with_cleanup(worker_id: str) -> Generator[DockerClient, None, None]:
    client = None
    try:
        with cleanup_all_new_docker_objects(CLIENT, worker_id):
            yield CLIENT
    finally:
        if client is not None:
            client.close()


@contextmanager
def cleanup_all_new_docker_objects(docker: DockerClient, worker_id: str):
    IMAGE_LABELS["io.prefect.test-worker"] = worker_id
    CONTAINER_LABELS["io.prefect.test-worker"] = worker_id
    try:
        yield
    finally:
        for container in docker.containers.list(all=True):
            if container.labels.get("io.prefect.test-worker") == worker_id:
                _safe_remove_container(container)
            elif container.labels.get("io.prefect.delete-me"):
                _safe_remove_container(container)

        filters = {"label": f"io.prefect.test-worker={worker_id}"}
        for image in docker.images.list(filters=filters):
            for tag in image.tags:
                docker.images.remove(tag, force=True)


def _safe_remove_container(container: Container):
    try:
        container.remove(force=True)
    except APIError:
        pass


@pytest.mark.flaky(max_runs=3)
async def test_container_result(
    docker_client_with_cleanup: "DockerClient",
    flow_run,
    default_docker_worker_job_configuration,
):
    async with DockerWorker(work_pool_name="test") as worker:
        result = await worker.run(
            flow_run=flow_run, configuration=default_docker_worker_job_configuration
        )
        assert bool(result)
        assert result.status_code == 0
        assert result.identifier
        _, container_id = worker._parse_infrastructure_pid(result.identifier)
        container = docker_client_with_cleanup.containers.get(container_id)
        assert container is not None


@pytest.mark.flaky(max_runs=3)
async def test_container_auto_remove(
    docker_client_with_cleanup: "DockerClient",
    flow_run,
    default_docker_worker_job_configuration,
):
    from docker.errors import NotFound

    default_docker_worker_job_configuration.auto_remove = True

    async with DockerWorker(work_pool_name="test") as worker:
        result = await worker.run(
            flow_run=flow_run, configuration=default_docker_worker_job_configuration
        )
        assert bool(result)
        assert result.status_code == 0
        assert result.identifier
        with pytest.raises(NotFound):
            _, container_id = worker._parse_infrastructure_pid(result.identifier)
            docker_client_with_cleanup.containers.get(container_id)


@pytest.mark.flaky(max_runs=3)
async def test_container_metadata(
    docker_client_with_cleanup: "DockerClient",
    flow_run,
    default_docker_worker_job_configuration,
):
    default_docker_worker_job_configuration.name = "test-container-name"
    default_docker_worker_job_configuration.labels = {"test.foo": "a", "test.bar": "b"}
    default_docker_worker_job_configuration.prepare_for_flow_run(flow_run=flow_run)
    async with DockerWorker(work_pool_name="test") as worker:
        result = await worker.run(
            flow_run=flow_run, configuration=default_docker_worker_job_configuration
        )

        _, container_id = worker._parse_infrastructure_pid(result.identifier)
    container: "Container" = docker_client_with_cleanup.containers.get(container_id)
    assert container.name == "test-container-name"
    assert container.labels["test.foo"] == "a"
    assert container.labels["test.bar"] == "b"
    assert container.image.tags[0] == get_prefect_image_name()

    for key, value in CONTAINER_LABELS.items():
        assert container.labels[key] == value


@pytest.mark.flaky(max_runs=3)
def test_real_auto_dockerfile_build(docker_client_with_cleanup):
    os.chdir(str(Path(__file__).parent / "test-project"))
    try:
        result = build_docker_image(
            image_name="local/repo", tag="test", dockerfile="auto", push=False
        )
        image: docker.models.images.Image = docker_client_with_cleanup.images.get(
            result["image"]
        )
        assert image

        cases = [
            {"command": "prefect version", "expected": prefect.__version__},
            {"command": "ls", "expected": "requirements.txt"},
        ]

        for case in cases:
            output = docker_client_with_cleanup.containers.run(
                image=result["image"],
                command=case["command"],
                labels=["prefect-docker-test"],
                remove=True,
            )
            assert case["expected"] in output.decode()

        output = docker_client_with_cleanup.containers.run(
            image=result["image"],
            command="python -c 'import pandas; print(pandas.__version__)'",
            labels=["prefect-docker-test"],
            remove=True,
        )
        if sys.version_info >= (3, 8):
            assert "2" in output.decode()
        else:
            assert "1" in output.decode()

    finally:
        docker_client_with_cleanup.containers.prune(
            filters={"label": "prefect-docker-test"}
        )
        image = docker_client_with_cleanup.images.get("local/repo:test")
        if image:
            docker_client_with_cleanup.images.remove(
                image="local/repo:test", force=True
            )


@pytest.mark.flaky(max_runs=3)
async def test_container_name_collision(
    docker_client_with_cleanup: "DockerClient",
    flow_run,
    default_docker_worker_job_configuration,
):
    # Generate a unique base name to avoid collissions with existing images
    base_name = uuid.uuid4().hex

    default_docker_worker_job_configuration.name = base_name
    default_docker_worker_job_configuration.auto_remove = False
    default_docker_worker_job_configuration.prepare_for_flow_run(flow_run)
    async with DockerWorker(work_pool_name="test") as worker:
        result = await worker.run(
            flow_run=flow_run, configuration=default_docker_worker_job_configuration
        )

        _, container_id = worker._parse_infrastructure_pid(result.identifier)
        created_container: "Container" = docker_client_with_cleanup.containers.get(
            container_id
        )
        assert created_container.name == base_name

        result = await worker.run(
            flow_run=flow_run, configuration=default_docker_worker_job_configuration
        )
        _, container_id = worker._parse_infrastructure_pid(result.identifier)
        created_container: "Container" = docker_client_with_cleanup.containers.get(
            container_id
        )
        assert created_container.name == base_name + "-1"


@pytest.mark.flaky(max_runs=3)
async def test_container_result_async(
    docker_client_with_cleanup: "DockerClient",
    flow_run,
    default_docker_worker_job_configuration,
):
    async with DockerWorker(work_pool_name="test") as worker:
        result = await worker.run(
            flow_run=flow_run, configuration=default_docker_worker_job_configuration
        )
        assert bool(result)
        assert result.status_code == 0
        assert result.identifier
        _, container_id = worker._parse_infrastructure_pid(result.identifier)
        container = docker_client_with_cleanup.containers.get(container_id)
        assert container is not None


@pytest.mark.flaky(max_runs=3)
async def test_stream_container_logs_on_real_container(
    capsys, flow_run, default_docker_worker_job_configuration
):
    default_docker_worker_job_configuration.command = "echo hello"
    async with DockerWorker(work_pool_name="test") as worker:
        await worker.run(
            flow_run=flow_run, configuration=default_docker_worker_job_configuration
        )

    captured = capsys.readouterr()
    assert "hello" in captured.out
