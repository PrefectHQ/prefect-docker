from prefect import flow

from prefect_docker.tasks import goodbye_prefect_docker, hello_prefect_docker


def test_hello_prefect_docker():
    @flow
    def test_flow():
        return hello_prefect_docker()

    result = test_flow()
    assert result == "Hello, prefect-docker!"


def goodbye_hello_prefect_docker():
    @flow
    def test_flow():
        return goodbye_prefect_docker()

    result = test_flow()
    assert result == "Goodbye, prefect-docker!"
