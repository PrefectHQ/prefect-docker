"""
This is a module containing tasks for interacting with:
Docker services
"""

# This module was auto-generated using prefect-collection-generator so
# manually editing this file is not recommended. If this module
# is outdated, rerun scripts/generate.py.

# OpenAPI spec: v1.41.yaml
# Updated at: 2022-08-17T00:00:42.747551

from typing import TYPE_CHECKING, Any, Dict, List, Union  # noqa

import httpx
from prefect import task

from prefect_docker.rest import HTTPMethod, execute_endpoint

if TYPE_CHECKING:
    from prefect_docker import DockerCredentials


@task
async def service_list(
    docker_credentials: "DockerCredentials",
    filters: str = None,
    status: bool = None,
) -> Dict[str, Any]:
    """
    List services.

    Args:
        docker_credentials:
            Credentials to use for authentication with Docker.
        filters:
            A JSON encoded value of the filters (a `map[string][]string`) to process
            on the services list.  Available filters:  - `id=<service
            id>` - `label=<service label>` -
            `mode=['replicated'|'global']` - `name=<service name>`.
        status:
            Include service status, with count of running and desired tasks.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/services`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | no error. |
    | 500 | server error. |
    | 503 | node is not part of a swarm. |
    """  # noqa
    endpoint = "/services"  # noqa

    responses = {
        200: "no error.",  # noqa
        500: "server error.",  # noqa
        503: "node is not part of a swarm.",  # noqa
    }

    params = {
        "filters": filters,
        "status": status,
    }

    try:
        response = await execute_endpoint.fn(
            endpoint,
            docker_credentials,
            http_method=HTTPMethod.GET,
            params=params,
        )
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        helpful_error_response = (responses or {}).get(response.status_code, "")
        try:
            helpful_error_response += f"JSON response: {response.json()}"
        except Exception:
            pass
        if helpful_error_response:
            raise httpx.HTTPStatusError(
                helpful_error_response, request=exc.request, response=exc.response
            ) from exc
        else:
            raise

    result = response.json()
    return result


@task
async def service_create(
    body: str,
    docker_credentials: "DockerCredentials",
    x_registry_auth: str = None,
) -> Dict[str, Any]:
    """
    Create a service.

    Args:
        body:

        docker_credentials:
            Credentials to use for authentication with Docker.
        x_registry_auth:
            A base64url-encoded auth configuration for pulling from private
            registries.  Refer to the [authentication section](
            section/Authentication) for details.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/services/create`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 201 | no error. |
    | 400 | bad parameter. |
    | 403 | network is not eligible for services. |
    | 409 | name conflicts with an existing service. |
    | 500 | server error. |
    | 503 | node is not part of a swarm. |
    """  # noqa
    endpoint = "/services/create"  # noqa

    responses = {
        201: "no error.",  # noqa
        400: "bad parameter.",  # noqa
        403: "network is not eligible for services.",  # noqa
        409: "name conflicts with an existing service.",  # noqa
        500: "server error.",  # noqa
        503: "node is not part of a swarm.",  # noqa
    }

    params = {
        "body": body,
        "x_registry_auth": x_registry_auth,
    }

    try:
        response = await execute_endpoint.fn(
            endpoint,
            docker_credentials,
            http_method=HTTPMethod.POST,
            params=params,
        )
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        helpful_error_response = (responses or {}).get(response.status_code, "")
        try:
            helpful_error_response += f"JSON response: {response.json()}"
        except Exception:
            pass
        if helpful_error_response:
            raise httpx.HTTPStatusError(
                helpful_error_response, request=exc.request, response=exc.response
            ) from exc
        else:
            raise

    result = response.json()
    return result


@task
async def service_inspect(
    id: str,
    docker_credentials: "DockerCredentials",
    insert_defaults: bool = False,
) -> Dict[str, Any]:
    """
    Inspect a service.

    Args:
        id:
            Id used in formatting the endpoint URL.
        docker_credentials:
            Credentials to use for authentication with Docker.
        insert_defaults:
            Fill empty fields with default values.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/services/{id}`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | no error. |
    | 404 | no such service. |
    | 500 | server error. |
    | 503 | node is not part of a swarm. |
    """  # noqa
    endpoint = f"/services/{id}"  # noqa
    responses = {
        200: "no error.",  # noqa
        404: "no such service.",  # noqa
        500: "server error.",  # noqa
        503: "node is not part of a swarm.",  # noqa
    }

    params = {
        "id": id,
        "insert_defaults": insert_defaults,
    }

    try:
        response = await execute_endpoint.fn(
            endpoint,
            docker_credentials,
            http_method=HTTPMethod.GET,
            params=params,
        )
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        helpful_error_response = (responses or {}).get(response.status_code, "")
        try:
            helpful_error_response += f"JSON response: {response.json()}"
        except Exception:
            pass
        if helpful_error_response:
            raise httpx.HTTPStatusError(
                helpful_error_response, request=exc.request, response=exc.response
            ) from exc
        else:
            raise

    result = response.json()
    return result


@task
async def service_delete(
    id: str,
    docker_credentials: "DockerCredentials",
) -> Dict[str, Any]:
    """
    Delete a service.

    Args:
        id:
            Id used in formatting the endpoint URL.
        docker_credentials:
            Credentials to use for authentication with Docker.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/services/{id}`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | no error. |
    | 404 | no such service. |
    | 500 | server error. |
    | 503 | node is not part of a swarm. |
    """  # noqa
    endpoint = f"/services/{id}"  # noqa
    responses = {
        200: "no error.",  # noqa
        404: "no such service.",  # noqa
        500: "server error.",  # noqa
        503: "node is not part of a swarm.",  # noqa
    }

    params = {
        "id": id,
    }

    try:
        response = await execute_endpoint.fn(
            endpoint,
            docker_credentials,
            http_method=HTTPMethod.DELETE,
            params=params,
        )
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        helpful_error_response = (responses or {}).get(response.status_code, "")
        try:
            helpful_error_response += f"JSON response: {response.json()}"
        except Exception:
            pass
        if helpful_error_response:
            raise httpx.HTTPStatusError(
                helpful_error_response, request=exc.request, response=exc.response
            ) from exc
        else:
            raise

    result = response.json()
    return result


@task
async def service_update(
    id: str,
    body: str,
    version: int,
    docker_credentials: "DockerCredentials",
    registry_auth_from: str = "spec",
    rollback: str = None,
    x_registry_auth: str = None,
) -> Dict[str, Any]:
    """
    Update a service.

    Args:
        id:
            Id used in formatting the endpoint URL.
        body:

        version:
            The version number of the service object being updated. This is required
            to avoid conflicting writes. This version number should be
            the value as currently set on the service *before* the
            update. You can find the current version by calling `GET
            /services/{id}`.
        docker_credentials:
            Credentials to use for authentication with Docker.
        registry_auth_from:
            If the `X-Registry-Auth` header is not specified, this parameter
            indicates where to find registry authorization credentials.
        rollback:
            Set to this parameter to `previous` to cause a server-side rollback to
            the previous service spec. The supplied spec will be ignored
            in this case.
        x_registry_auth:
            A base64url-encoded auth configuration for pulling from private
            registries.  Refer to the [authentication section](
            section/Authentication) for details.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/services/{id}/update`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | no error. |
    | 400 | bad parameter. |
    | 404 | no such service. |
    | 500 | server error. |
    | 503 | node is not part of a swarm. |
    """  # noqa
    endpoint = f"/services/{id}/update"  # noqa
    responses = {
        200: "no error.",  # noqa
        400: "bad parameter.",  # noqa
        404: "no such service.",  # noqa
        500: "server error.",  # noqa
        503: "node is not part of a swarm.",  # noqa
    }

    params = {
        "id": id,
        "body": body,
        "version": version,
        "registry_auth_from": registry_auth_from,
        "rollback": rollback,
        "x_registry_auth": x_registry_auth,
    }

    try:
        response = await execute_endpoint.fn(
            endpoint,
            docker_credentials,
            http_method=HTTPMethod.POST,
            params=params,
        )
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        helpful_error_response = (responses or {}).get(response.status_code, "")
        try:
            helpful_error_response += f"JSON response: {response.json()}"
        except Exception:
            pass
        if helpful_error_response:
            raise httpx.HTTPStatusError(
                helpful_error_response, request=exc.request, response=exc.response
            ) from exc
        else:
            raise

    result = response.json()
    return result


@task
async def service_logs(
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
    Get `stdout` and `stderr` logs from a service. See also
    [`/containers/{id}/logs`](
    operation/ContainerLogs).  **Note**: This endpoint works only for services
    with the `local`, `json-file` or `journald` logging drivers.

    Args:
        id:
            Id used in formatting the endpoint URL.
        docker_credentials:
            Credentials to use for authentication with Docker.
        details:
            Show service context and extra details provided to logs.
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
    `/services/{id}/logs`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | logs returned as a stream in response body. |
    | 404 | no such service. |
    | 500 | server error. |
    | 503 | node is not part of a swarm. |
    """  # noqa
    endpoint = f"/services/{id}/logs"  # noqa
    responses = {
        200: "logs returned as a stream in response body.",  # noqa
        404: "no such service.",  # noqa
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

    try:
        response = await execute_endpoint.fn(
            endpoint,
            docker_credentials,
            http_method=HTTPMethod.GET,
            params=params,
        )
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        helpful_error_response = (responses or {}).get(response.status_code, "")
        try:
            helpful_error_response += f"JSON response: {response.json()}"
        except Exception:
            pass
        if helpful_error_response:
            raise httpx.HTTPStatusError(
                helpful_error_response, request=exc.request, response=exc.response
            ) from exc
        else:
            raise

    result = response.json()
    return result
