"""
This is a module containing tasks for interacting with:
Docker nodes
"""

# This module was auto-generated using prefect-collection-generator so
# manually editing this file is not recommended. If this module
# is outdated, rerun scripts/generate.py.

# OpenAPI spec: v1.41.yaml
# Updated at: 2022-08-18T00:04:16.563073

from typing import TYPE_CHECKING, Any, Dict, List, Union  # noqa

from prefect import task

from prefect_docker.rest import HTTPMethod, _unpack_contents, execute_endpoint

if TYPE_CHECKING:
    from prefect_docker import DockerCredentials


@task
async def node_list(
    docker_credentials: "DockerCredentials",
    filters: str = None,
) -> Dict[str, Any]:
    """
    List nodes.

    Args:
        docker_credentials:
            Credentials to use for authentication with Docker.
        filters:
            Filters to process on the nodes list, encoded as JSON (a
            `map[string][]string`).  Available filters: - `id=<node id>`
            - `label=<engine label>` -
            `membership=`(`accepted`|`pending`)` - `name=<node name>` -
            `node.label=<node label>` - `role=`(`manager`|`worker`)`.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/nodes`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | no error. |
    | 500 | server error. |
    | 503 | node is not part of a swarm. |
    """  # noqa
    endpoint = "/nodes"  # noqa

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
async def node_inspect(
    id: str,
    docker_credentials: "DockerCredentials",
) -> Dict[str, Any]:
    """
    Inspect a node.

    Args:
        id:
            Id used in formatting the endpoint URL.
        docker_credentials:
            Credentials to use for authentication with Docker.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/nodes/{id}`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | no error. |
    | 404 | no such node. |
    | 500 | server error. |
    | 503 | node is not part of a swarm. |
    """  # noqa
    endpoint = f"/nodes/{id}"  # noqa
    responses = {
        200: "no error.",  # noqa
        404: "no such node.",  # noqa
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
async def node_delete(
    id: str,
    docker_credentials: "DockerCredentials",
    force: bool = False,
) -> Dict[str, Any]:
    """
    Delete a node.

    Args:
        id:
            Id used in formatting the endpoint URL.
        docker_credentials:
            Credentials to use for authentication with Docker.
        force:
            Force remove a node from the swarm.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/nodes/{id}`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | no error. |
    | 404 | no such node. |
    | 500 | server error. |
    | 503 | node is not part of a swarm. |
    """  # noqa
    endpoint = f"/nodes/{id}"  # noqa
    responses = {
        200: "no error.",  # noqa
        404: "no such node.",  # noqa
        500: "server error.",  # noqa
        503: "node is not part of a swarm.",  # noqa
    }

    params = {
        "id": id,
        "force": force,
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
async def node_update(
    id: str,
    version: int,
    docker_credentials: "DockerCredentials",
    body: str = None,
) -> Dict[str, Any]:
    """
    Update a node.

    Args:
        id:
            Id used in formatting the endpoint URL.
        version:
            The version number of the node object being updated. This is required to
            avoid conflicting writes.
        docker_credentials:
            Credentials to use for authentication with Docker.
        body:


    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/nodes/{id}/update`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | no error. |
    | 400 | bad parameter. |
    | 404 | no such node. |
    | 500 | server error. |
    | 503 | node is not part of a swarm. |
    """  # noqa
    endpoint = f"/nodes/{id}/update"  # noqa
    responses = {
        200: "no error.",  # noqa
        400: "bad parameter.",  # noqa
        404: "no such node.",  # noqa
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
