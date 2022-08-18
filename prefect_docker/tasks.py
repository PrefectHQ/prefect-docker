"""
This is a module containing tasks for interacting with:
Docker tasks
"""

# This module was auto-generated using prefect-collection-generator so
# manually editing this file is not recommended. If this module
# is outdated, rerun scripts/generate.py.

# OpenAPI spec: v1.41.yaml
# Updated at: 2022-08-18T00:04:16.567494

from typing import TYPE_CHECKING, Any, Dict, List, Union  # noqa

from prefect import task

from prefect_docker.rest import HTTPMethod, _unpack_contents, execute_endpoint

if TYPE_CHECKING:
    from prefect_docker import DockerCredentials


@task
async def task_list(
    docker_credentials: "DockerCredentials",
    filters: str = None,
) -> Dict[str, Any]:
    """
    List tasks.

    Args:
        docker_credentials:
            Credentials to use for authentication with Docker.
        filters:
            A JSON encoded value of the filters (a `map[string][]string`) to process
            on the tasks list.  Available filters:  - `desired-
            state=(running | shutdown | accepted)` - `id=<task id>` -
            `label=key` or `label='key=value'` - `name=<task name>` -
            `node=<node id or name>` - `service=<service name>`.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/tasks`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | no error. |
    | 500 | server error. |
    | 503 | node is not part of a swarm. |
    """  # noqa
    endpoint = "/tasks"  # noqa

    responses = {
        200: "no error.",  # noqa
        500: "server error.",  # noqa
        503: "node is not part of a swarm.",  # noqa
    }

    params = {
        "filters": filters,
    }

    response = await execute_endpoint.fn(
        endpoint,
        docker_credentials,
        http_method=HTTPMethod.GET,
        params=params,
    )

    contents = _unpack_contents(response, responses)
    return contents


@task
async def task_inspect(
    id: str,
    docker_credentials: "DockerCredentials",
) -> Dict[str, Any]:
    """
    Inspect a task.

    Args:
        id:
            Id used in formatting the endpoint URL.
        docker_credentials:
            Credentials to use for authentication with Docker.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/tasks/{id}`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | no error. |
    | 404 | no such task. |
    | 500 | server error. |
    | 503 | node is not part of a swarm. |
    """  # noqa
    endpoint = f"/tasks/{id}"  # noqa
    responses = {
        200: "no error.",  # noqa
        404: "no such task.",  # noqa
        500: "server error.",  # noqa
        503: "node is not part of a swarm.",  # noqa
    }

    params = {
        "id": id,
    }

    response = await execute_endpoint.fn(
        endpoint,
        docker_credentials,
        http_method=HTTPMethod.GET,
        params=params,
    )

    contents = _unpack_contents(response, responses)
    return contents


@task
async def task_logs(
    id: str,
    docker_credentials: "DockerCredentials",
    details: bool = False,
    follow: bool = False,
    stdout: bool = False,
    stderr: bool = False,
    since: int = 0,
    timestamps: bool = False,
    tail: str = "all",
) -> Dict[str, Any]:
    """
    Get `stdout` and `stderr` logs from a task. See also [`/containers/{id}/logs`](
    operation/ContainerLogs).  **Note**: This endpoint works only for services
    with the `local`, `json-file` or `journald` logging drivers.

    Args:
        id:
            Id used in formatting the endpoint URL.
        docker_credentials:
            Credentials to use for authentication with Docker.
        details:
            Show task context and extra details provided to logs.
        follow:
            Keep connection after returning logs.
        stdout:
            Return logs from `stdout`.
        stderr:
            Return logs from `stderr`.
        since:
            Only return logs since this time, as a UNIX timestamp.
        timestamps:
            Add timestamps to every log line.
        tail:
            Only return this number of log lines from the end of the logs. Specify
            as an integer or `all` to output all log lines.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/tasks/{id}/logs`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | logs returned as a stream in response body. |
    | 404 | no such task. |
    | 500 | server error. |
    | 503 | node is not part of a swarm. |
    """  # noqa
    endpoint = f"/tasks/{id}/logs"  # noqa
    responses = {
        200: "logs returned as a stream in response body.",  # noqa
        404: "no such task.",  # noqa
        500: "server error.",  # noqa
        503: "node is not part of a swarm.",  # noqa
    }

    params = {
        "id": id,
        "details": details,
        "follow": follow,
        "stdout": stdout,
        "stderr": stderr,
        "since": since,
        "timestamps": timestamps,
        "tail": tail,
    }

    response = await execute_endpoint.fn(
        endpoint,
        docker_credentials,
        http_method=HTTPMethod.GET,
        params=params,
    )

    contents = _unpack_contents(response, responses)
    return contents
