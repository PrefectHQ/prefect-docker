"""
This is a module containing tasks for interacting with:
Docker volumes
"""

# This module was auto-generated using prefect-collection-generator so
# manually editing this file is not recommended. If this module
# is outdated, rerun scripts/generate.py.

# OpenAPI spec: v1.41.yaml
# Updated at: 2022-08-17T00:00:42.734677

from typing import TYPE_CHECKING, Any, Dict, List, Union  # noqa

import httpx
from prefect import task

from prefect_docker.rest import HTTPMethod, execute_endpoint

if TYPE_CHECKING:
    from prefect_docker import DockerCredentials


@task
async def volume_list(
    docker_credentials: "DockerCredentials",
    filters: str = None,
) -> Dict[str, Any]:
    """
    List volumes.

    Args:
        docker_credentials:
            Credentials to use for authentication with Docker.
        filters:
            JSON encoded value of the filters (a `map[string][]string`) to process
            on the volumes list. Available filters:  -
            `dangling=<boolean>` When set to `true` (or `1`), returns
            all    volumes that are not in use by a container. When set
            to `false`    (or `0`), only volumes that are in use by one
            or more    containers are returned. - `driver=<volume-
            driver-name>` Matches volumes based on their driver. -
            `label=<key>` or `label=<key>:<value>` Matches volumes based
            on    the presence of a `label` alone or a `label` and a
            value. - `name=<volume-name>` Matches all or part of a
            volume name.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/volumes`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | Summary volume data that matches the query. |
    | 500 | Server error. |
    """  # noqa
    endpoint = "/volumes"  # noqa

    responses = {
        200: "Summary volume data that matches the query.",  # noqa
        500: "Server error.",  # noqa
    }

    params = {
        "filters": filters,
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
async def volume_create(
    volume_config: str,
    docker_credentials: "DockerCredentials",
) -> Dict[str, Any]:
    """
    Create a volume.

    Args:
        volume_config:
            Volume configuration.
        docker_credentials:
            Credentials to use for authentication with Docker.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/volumes/create`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 201 | The volume was created successfully. |
    | 500 | Server error. |
    """  # noqa
    endpoint = "/volumes/create"  # noqa

    responses = {
        201: "The volume was created successfully.",  # noqa
        500: "Server error.",  # noqa
    }

    params = {
        "volume_config": volume_config,
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
async def volume_inspect(
    name: str,
    docker_credentials: "DockerCredentials",
) -> Dict[str, Any]:
    """
    Inspect a volume.

    Args:
        name:
            Name used in formatting the endpoint URL.
        docker_credentials:
            Credentials to use for authentication with Docker.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/volumes/{name}`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | No error. |
    | 404 | No such volume. |
    | 500 | Server error. |
    """  # noqa
    endpoint = f"/volumes/{name}"  # noqa
    responses = {
        200: "No error.",  # noqa
        404: "No such volume.",  # noqa
        500: "Server error.",  # noqa
    }

    params = {
        "name": name,
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
async def volume_delete(
    name: str,
    docker_credentials: "DockerCredentials",
    force: bool = False,
) -> Dict[str, Any]:
    """
    Instruct the driver to remove the volume.

    Args:
        name:
            Name used in formatting the endpoint URL.
        docker_credentials:
            Credentials to use for authentication with Docker.
        force:
            Force the removal of the volume.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/volumes/{name}`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 204 | The volume was removed. |
    | 404 | No such volume or volume driver. |
    | 409 | Volume is in use and cannot be removed. |
    | 500 | Server error. |
    """  # noqa
    endpoint = f"/volumes/{name}"  # noqa
    responses = {
        204: "The volume was removed.",  # noqa
        404: "No such volume or volume driver.",  # noqa
        409: "Volume is in use and cannot be removed.",  # noqa
        500: "Server error.",  # noqa
    }

    params = {
        "name": name,
        "force": force,
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
async def volume_prune(
    docker_credentials: "DockerCredentials",
    filters: str = None,
) -> Dict[str, Any]:
    """
    Delete unused volumes.

    Args:
        docker_credentials:
            Credentials to use for authentication with Docker.
        filters:
            Filters to process on the prune list, encoded as JSON (a
            `map[string][]string`).  Available filters: - `label`
            (`label=<key>`, `label=<key>=<value>`, `label!=<key>`, or
            `label!=<key>=<value>`) Prune volumes with (or without, in
            case `label!=...` is used) the specified labels.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/volumes/prune`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | No error. |
    | 500 | Server error. |
    """  # noqa
    endpoint = "/volumes/prune"  # noqa

    responses = {
        200: "No error.",  # noqa
        500: "Server error.",  # noqa
    }

    params = {
        "filters": filters,
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
