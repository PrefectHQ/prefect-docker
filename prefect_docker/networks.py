"""
This is a module containing tasks for interacting with:
Docker networks
"""

# This module was auto-generated using prefect-collection-generator so
# manually editing this file is not recommended. If this module
# is outdated, rerun scripts/generate.py.

# OpenAPI spec: v1.41.yaml
# Updated at: 2022-08-18T00:04:16.558691

from typing import TYPE_CHECKING, Any, Dict, List, Union  # noqa

from prefect import task

from prefect_docker.rest import HTTPMethod, _unpack_contents, execute_endpoint

if TYPE_CHECKING:
    from prefect_docker import DockerCredentials


@task
async def network_list(
    docker_credentials: "DockerCredentials",
    filters: str = None,
) -> Dict[str, Any]:
    """
    Returns a list of networks. For details on the format, see the [network inspect
    endpoint](
    operation/NetworkInspect).  Note that it uses a different, smaller
    representation of a network than inspecting a single network. For example,
    the list of containers attached to the network is not propagated in API
    versions 1.28 and up.

    Args:
        docker_credentials:
            Credentials to use for authentication with Docker.
        filters:
            JSON encoded value of the filters (a `map[string][]string`) to process
            on the networks list.  Available filters:  -
            `dangling=<boolean>` When set to `true` (or `1`), returns
            all    networks that are not in use by a container. When set
            to `false`    (or `0`), only networks that are in use by one
            or more    containers are returned. - `driver=<driver-name>`
            Matches a network's driver. - `id=<network-id>` Matches all
            or part of a network ID. - `label=<key>` or
            `label=<key>=<value>` of a network label. - `name=<network-
            name>` Matches all or part of a network name. -
            `scope=['swarm'|'global'|'local']` Filters networks by scope
            (`swarm`, `global`, or `local`). -
            `type=['custom'|'builtin']` Filters networks by type. The
            `custom` keyword returns all user-defined networks.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/networks`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | No error. |
    | 500 | Server error. |
    """  # noqa
    endpoint = "/networks"  # noqa

    responses = {
        200: "No error.",  # noqa
        500: "Server error.",  # noqa
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
async def network_inspect(
    id: str,
    docker_credentials: "DockerCredentials",
    verbose: bool = False,
    scope: str = None,
) -> Dict[str, Any]:
    """
    Inspect a network.

    Args:
        id:
            Id used in formatting the endpoint URL.
        docker_credentials:
            Credentials to use for authentication with Docker.
        verbose:
            Detailed inspect output for troubleshooting.
        scope:
            Filter the network by scope (swarm, global, or local).

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/networks/{id}`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | No error. |
    | 404 | Network not found. |
    | 500 | Server error. |
    """  # noqa
    endpoint = f"/networks/{id}"  # noqa
    responses = {
        200: "No error.",  # noqa
        404: "Network not found.",  # noqa
        500: "Server error.",  # noqa
    }

    params = {
        "id": id,
        "verbose": verbose,
        "scope": scope,
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
async def network_delete(
    id: str,
    docker_credentials: "DockerCredentials",
) -> Dict[str, Any]:
    """
    Remove a network.

    Args:
        id:
            Id used in formatting the endpoint URL.
        docker_credentials:
            Credentials to use for authentication with Docker.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/networks/{id}`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 204 | No error. |
    | 403 | operation not supported for pre-defined networks. |
    | 404 | no such network. |
    | 500 | Server error. |
    """  # noqa
    endpoint = f"/networks/{id}"  # noqa
    responses = {
        204: "No error.",  # noqa
        403: "operation not supported for pre-defined networks.",  # noqa
        404: "no such network.",  # noqa
        500: "Server error.",  # noqa
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
async def network_create(
    network_config: Dict,
    docker_credentials: "DockerCredentials",
) -> Dict[str, Any]:
    """
    Create a network.

    Args:
        network_config:
            Network configuration.
        docker_credentials:
            Credentials to use for authentication with Docker.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/networks/create`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 201 | No error. |
    | 403 | operation not supported for pre-defined networks. |
    | 404 | plugin not found. |
    | 500 | Server error. |
    """  # noqa
    endpoint = "/networks/create"  # noqa

    responses = {
        201: "No error.",  # noqa
        403: "operation not supported for pre-defined networks.",  # noqa
        404: "plugin not found.",  # noqa
        500: "Server error.",  # noqa
    }

    params = {
        "network_config": network_config,
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
async def network_connect(
    id: str,
    container: Dict,
    docker_credentials: "DockerCredentials",
) -> Dict[str, Any]:
    """
    Connect a container to a network.

    Args:
        id:
            Id used in formatting the endpoint URL.
        container:

        docker_credentials:
            Credentials to use for authentication with Docker.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/networks/{id}/connect`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | No error. |
    | 403 | Operation not supported for swarm scoped networks. |
    | 404 | Network or container not found. |
    | 500 | Server error. |
    """  # noqa
    endpoint = f"/networks/{id}/connect"  # noqa
    responses = {
        200: "No error.",  # noqa
        403: "Operation not supported for swarm scoped networks.",  # noqa
        404: "Network or container not found.",  # noqa
        500: "Server error.",  # noqa
    }

    params = {
        "id": id,
        "container": container,
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
async def network_disconnect(
    id: str,
    container: Dict,
    docker_credentials: "DockerCredentials",
) -> Dict[str, Any]:
    """
    Disconnect a container from a network.

    Args:
        id:
            Id used in formatting the endpoint URL.
        container:

        docker_credentials:
            Credentials to use for authentication with Docker.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/networks/{id}/disconnect`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | No error. |
    | 403 | Operation not supported for swarm scoped networks. |
    | 404 | Network or container not found. |
    | 500 | Server error. |
    """  # noqa
    endpoint = f"/networks/{id}/disconnect"  # noqa
    responses = {
        200: "No error.",  # noqa
        403: "Operation not supported for swarm scoped networks.",  # noqa
        404: "Network or container not found.",  # noqa
        500: "Server error.",  # noqa
    }

    params = {
        "id": id,
        "container": container,
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
async def network_prune(
    docker_credentials: "DockerCredentials",
    filters: str = None,
) -> Dict[str, Any]:
    """
    Delete unused networks.

    Args:
        docker_credentials:
            Credentials to use for authentication with Docker.
        filters:
            Filters to process on the prune list, encoded as JSON (a
            `map[string][]string`).  Available filters: -
            `until=<timestamp>` Prune networks created before this
            timestamp. The `<timestamp>` can be Unix timestamps, date
            formatted timestamps, or Go duration strings (e.g. `10m`,
            `1h30m`) computed relative to the daemon machine’s time. -
            `label` (`label=<key>`, `label=<key>=<value>`,
            `label!=<key>`, or `label!=<key>=<value>`) Prune networks
            with (or without, in case `label!=...` is used) the
            specified labels.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/networks/prune`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | No error. |
    | 500 | Server error. |
    """  # noqa
    endpoint = "/networks/prune"  # noqa

    responses = {
        200: "No error.",  # noqa
        500: "Server error.",  # noqa
    }

    params = {
        "filters": filters,
    }

    response = await execute_endpoint.fn(
        endpoint,
        docker_credentials,
        http_method=HTTPMethod.POST,
        params=params,
    )

    contents = _unpack_contents(response, responses)
    return contents
