"""
This is a module containing tasks for interacting with:
Docker configs
"""

# This module was auto-generated using prefect-collection-generator so
# manually editing this file is not recommended. If this module
# is outdated, rerun scripts/generate.py.

# OpenAPI spec: v1.41.yaml
# Updated at: 2022-08-18T00:04:16.569719

from typing import TYPE_CHECKING, Any, Dict, List, Union  # noqa

from prefect import task

from prefect_docker.rest import HTTPMethod, _unpack_contents, execute_endpoint

if TYPE_CHECKING:
    from prefect_docker import DockerCredentials


@task
async def config_list(
    docker_credentials: "DockerCredentials",
    filters: str = None,
) -> Dict[str, Any]:
    """
    List configs.

    Args:
        docker_credentials:
            Credentials to use for authentication with Docker.
        filters:
            A JSON encoded value of the filters (a `map[string][]string`) to process
            on the configs list.  Available filters:  - `id=<config id>`
            - `label=<key> or label=<key>=value` - `name=<config name>`
            - `names=<config name>`.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/configs`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | no error. |
    | 500 | server error. |
    | 503 | node is not part of a swarm. |
    """  # noqa
    endpoint = "/configs"  # noqa

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
async def config_create(
    docker_credentials: "DockerCredentials",
    body: str = None,
) -> Dict[str, Any]:
    """
    Create a config.

    Args:
        docker_credentials:
            Credentials to use for authentication with Docker.
        body:


    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/configs/create`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 201 | no error. |
    | 409 | name conflicts with an existing object. |
    | 500 | server error. |
    | 503 | node is not part of a swarm. |
    """  # noqa
    endpoint = "/configs/create"  # noqa

    responses = {
        201: "no error.",  # noqa
        409: "name conflicts with an existing object.",  # noqa
        500: "server error.",  # noqa
        503: "node is not part of a swarm.",  # noqa
    }

    params = {
        "body": body,
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
async def config_inspect(
    id: str,
    docker_credentials: "DockerCredentials",
) -> Dict[str, Any]:
    """
    Inspect a config.

    Args:
        id:
            Id used in formatting the endpoint URL.
        docker_credentials:
            Credentials to use for authentication with Docker.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/configs/{id}`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | no error. |
    | 404 | config not found. |
    | 500 | server error. |
    | 503 | node is not part of a swarm. |
    """  # noqa
    endpoint = f"/configs/{id}"  # noqa
    responses = {
        200: "no error.",  # noqa
        404: "config not found.",  # noqa
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
async def config_delete(
    id: str,
    docker_credentials: "DockerCredentials",
) -> Dict[str, Any]:
    """
    Delete a config.

    Args:
        id:
            Id used in formatting the endpoint URL.
        docker_credentials:
            Credentials to use for authentication with Docker.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/configs/{id}`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 204 | no error. |
    | 404 | config not found. |
    | 500 | server error. |
    | 503 | node is not part of a swarm. |
    """  # noqa
    endpoint = f"/configs/{id}"  # noqa
    responses = {
        204: "no error.",  # noqa
        404: "config not found.",  # noqa
        500: "server error.",  # noqa
        503: "node is not part of a swarm.",  # noqa
    }

    params = {
        "id": id,
    }

    response = await execute_endpoint.fn(
        endpoint,
        docker_credentials,
        http_method=HTTPMethod.DELETE,
        params=params,
    )

    contents = _unpack_contents(response, responses)
    return contents


@task
async def config_update(
    id: str,
    version: int,
    docker_credentials: "DockerCredentials",
    body: str = None,
) -> Dict[str, Any]:
    """
    Update a Config.

    Args:
        id:
            Id used in formatting the endpoint URL.
        version:
            The version number of the config object being updated. This is required
            to avoid conflicting writes.
        docker_credentials:
            Credentials to use for authentication with Docker.
        body:
            The spec of the config to update. Currently, only the Labels field can
            be updated. All other fields must remain unchanged from the
            [ConfigInspect endpoint](
            operation/ConfigInspect) response values.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/configs/{id}/update`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | no error. |
    | 400 | bad parameter. |
    | 404 | no such config. |
    | 500 | server error. |
    | 503 | node is not part of a swarm. |
    """  # noqa
    endpoint = f"/configs/{id}/update"  # noqa
    responses = {
        200: "no error.",  # noqa
        400: "bad parameter.",  # noqa
        404: "no such config.",  # noqa
        500: "server error.",  # noqa
        503: "node is not part of a swarm.",  # noqa
    }

    params = {
        "id": id,
        "body": body,
        "version": version,
    }

    response = await execute_endpoint.fn(
        endpoint,
        docker_credentials,
        http_method=HTTPMethod.POST,
        params=params,
    )

    contents = _unpack_contents(response, responses)
    return contents
