"""
This is a module containing tasks for interacting with:
Docker exec
"""

# This module was auto-generated using prefect-collection-generator so
# manually editing this file is not recommended. If this module
# is outdated, rerun scripts/generate.py.

# OpenAPI spec: v1.41.yaml
# Updated at: 2022-08-18T00:04:16.556592

from typing import TYPE_CHECKING, Any, Dict, List, Union  # noqa

from prefect import task

from prefect_docker.rest import HTTPMethod, _unpack_contents, execute_endpoint

if TYPE_CHECKING:
    from prefect_docker import DockerCredentials


@task
async def exec_start(
    id: str,
    docker_credentials: "DockerCredentials",
    exec_start_config: Dict = None,
) -> Dict[str, Any]:
    """
    Starts a previously set up exec instance. If detach is true, this endpoint
    returns immediately after starting the command. Otherwise, it sets up an
    interactive session with the command.

    Args:
        id:
            Id used in formatting the endpoint URL.
        docker_credentials:
            Credentials to use for authentication with Docker.
        exec_start_config:


    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/exec/{id}/start`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | No error. |
    | 404 | No such exec instance. |
    | 409 | Container is stopped or paused. |
    """  # noqa
    endpoint = f"/exec/{id}/start"  # noqa
    responses = {
        200: "No error.",  # noqa
        404: "No such exec instance.",  # noqa
        409: "Container is stopped or paused.",  # noqa
    }

    params = {
        "exec_start_config": exec_start_config,
        "id": id,
    }

    response = await execute_endpoint.fn(
        endpoint,
        docker_credentials,
        http_method=HTTPMethod.POST,
        params=params,
    )

    contents = _unpack_contents(response, responses)
    return contents


@task
async def exec_resize(
    id: str,
    docker_credentials: "DockerCredentials",
    h: int = None,
    w: int = None,
) -> Dict[str, Any]:
    """
    Resize the TTY session used by an exec instance. This endpoint only works if
    `tty` was specified as part of creating and starting the exec instance.

    Args:
        id:
            Id used in formatting the endpoint URL.
        docker_credentials:
            Credentials to use for authentication with Docker.
        h:
            Height of the TTY session in characters.
        w:
            Width of the TTY session in characters.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/exec/{id}/resize`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | No error. |
    | 400 | bad parameter. |
    | 404 | No such exec instance. |
    | 500 | Server error. |
    """  # noqa
    endpoint = f"/exec/{id}/resize"  # noqa
    responses = {
        200: "No error.",  # noqa
        400: "bad parameter.",  # noqa
        404: "No such exec instance.",  # noqa
        500: "Server error.",  # noqa
    }

    params = {
        "id": id,
        "h": h,
        "w": w,
    }

    response = await execute_endpoint.fn(
        endpoint,
        docker_credentials,
        http_method=HTTPMethod.POST,
        params=params,
    )

    contents = _unpack_contents(response, responses)
    return contents


@task
async def exec_inspect(
    id: str,
    docker_credentials: "DockerCredentials",
) -> Dict[str, Any]:
    """
    Return low-level information about an exec instance.

    Args:
        id:
            Id used in formatting the endpoint URL.
        docker_credentials:
            Credentials to use for authentication with Docker.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/exec/{id}/json`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | No error. |
    | 404 | No such exec instance. |
    | 500 | Server error. |
    """  # noqa
    endpoint = f"/exec/{id}/json"  # noqa
    responses = {
        200: "No error.",  # noqa
        404: "No such exec instance.",  # noqa
        500: "Server error.",  # noqa
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
