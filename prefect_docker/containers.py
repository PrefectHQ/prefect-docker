"""
This is a module containing tasks for interacting with:
Docker containers
"""

# This module was auto-generated using prefect-collection-generator so
# manually editing this file is not recommended. If this module
# is outdated, rerun scripts/generate.py.

# OpenAPI spec: v1.41.yaml
# Updated at: 2022-08-18T00:04:16.537758

from typing import TYPE_CHECKING, Any, Dict, List, Union  # noqa

from prefect import task

from prefect_docker.rest import HTTPMethod, _unpack_contents, execute_endpoint

if TYPE_CHECKING:
    from prefect_docker import DockerCredentials


@task
async def container_list(
    docker_credentials: "DockerCredentials",
    all: bool = False,
    limit: int = None,
    size: bool = False,
    filters: str = None,
) -> Dict[str, Any]:
    """
    Returns a list of containers. For details on the format, see the [inspect
    endpoint](
    operation/ContainerInspect).  Note that it uses a different, smaller
    representation of a container than inspecting a single container. For
    example, the list of linked containers is not propagated .

    Args:
        docker_credentials:
            Credentials to use for authentication with Docker.
        all:
            Return all containers. By default, only running containers are shown.
        limit:
            Return this number of most recently created containers, including non-
            running ones.
        size:
            Return the size of container as fields `SizeRw` and `SizeRootFs`.
        filters:
            Filters to process on the container list, encoded as JSON (a
            `map[string][]string`). For example, `{'status':
            ['paused']}` will only return paused containers.  Available
            filters:  - `ancestor`=(`<image-name>[:<tag>]`, `<image
            id>`, or `<image@digest>`) - `before`=(`<container id>` or
            `<container name>`) -
            `expose`=(`<port>[/<proto>]`|`<startport-
            endport>/[<proto>]`) - `exited=<int>` containers with exit
            code of `<int>` -
            `health`=(`starting`|`healthy`|`unhealthy`|`none`) -
            `id=<ID>` a container's ID -
            `isolation=`(`default`|`process`|`hyperv`) (Windows daemon
            only) - `is-task=`(`true`|`false`) - `label=key` or
            `label='key=value'` of a container label - `name=<name>` a
            container's name - `network`=(`<network id>` or `<network
            name>`) - `publish`=(`<port>[/<proto>]`|`<startport-
            endport>/[<proto>]`) - `since`=(`<container id>` or
            `<container name>`) -
            `status=`(`created`|`restarting`|`running`|`removing`|`paused`|`exited`|`dead`)
            - `volume`=(`<volume name>` or `<mount point destination>`).

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/containers/json`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | no error. |
    | 400 | bad parameter. |
    | 500 | server error. |
    """  # noqa
    endpoint = "/containers/json"  # noqa

    responses = {
        200: "no error.",  # noqa
        400: "bad parameter.",  # noqa
        500: "server error.",  # noqa
    }

    params = {
        "all": all,
        "limit": limit,
        "size": size,
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
async def container_create(
    body: str,
    docker_credentials: "DockerCredentials",
    name: str = None,
    platform: str = None,
) -> Dict[str, Any]:
    """
    Create a container.

    Args:
        body:
            Container to create.
        docker_credentials:
            Credentials to use for authentication with Docker.
        name:
            Assign the specified name to the container. Must match
            `/?[a-zA-Z0-9][a-zA-Z0-9_.-]+`.
        platform:
            Platform in the format `os[/arch[/variant]]` used for image lookup.
            When specified, the daemon checks if the requested image is
            present in the local image cache with the given OS and
            Architecture, and otherwise returns a `404` status.  If the
            option is not set, the host's native OS and Architecture are
            used to look up the image in the image cache. However, if no
            platform is passed and the given image does exist in the
            local image cache, but its OS or architecture does not
            match, the container is created with the available image,
            and a warning is added to the `Warnings` field in the
            response, for example;      WARNING: The requested image's
            platform (linux/arm64/v8) does not              match the
            detected host platform (linux/amd64) and no
            specific platform was requested.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/containers/create`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 201 | Container created successfully. |
    | 400 | bad parameter. |
    | 404 | no such image. |
    | 409 | conflict. |
    | 500 | server error. |
    """  # noqa
    endpoint = "/containers/create"  # noqa

    responses = {
        201: "Container created successfully.",  # noqa
        400: "bad parameter.",  # noqa
        404: "no such image.",  # noqa
        409: "conflict.",  # noqa
        500: "server error.",  # noqa
    }

    params = {
        "name": name,
        "platform": platform,
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
async def container_inspect(
    id: str,
    docker_credentials: "DockerCredentials",
    size: bool = False,
) -> Dict[str, Any]:
    """
    Return low-level information about a container.

    Args:
        id:
            Id used in formatting the endpoint URL.
        docker_credentials:
            Credentials to use for authentication with Docker.
        size:
            Return the size of container as fields `SizeRw` and `SizeRootFs`.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/containers/{id}/json`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | no error. |
    | 404 | no such container. |
    | 500 | server error. |
    """  # noqa
    endpoint = f"/containers/{id}/json"  # noqa
    responses = {
        200: "no error.",  # noqa
        404: "no such container.",  # noqa
        500: "server error.",  # noqa
    }

    params = {
        "id": id,
        "size": size,
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
async def container_top(
    id: str,
    docker_credentials: "DockerCredentials",
    ps_args: str = "-ef",
) -> Dict[str, Any]:
    """
    On Unix systems, this is done by running the `ps` command. This endpoint is not
    supported on Windows.

    Args:
        id:
            Id used in formatting the endpoint URL.
        docker_credentials:
            Credentials to use for authentication with Docker.
        ps_args:
            The arguments to pass to `ps`. For example, `aux`.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/containers/{id}/top`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | no error. |
    | 404 | no such container. |
    | 500 | server error. |
    """  # noqa
    endpoint = f"/containers/{id}/top"  # noqa
    responses = {
        200: "no error.",  # noqa
        404: "no such container.",  # noqa
        500: "server error.",  # noqa
    }

    params = {
        "id": id,
        "ps_args": ps_args,
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
async def container_logs(
    id: str,
    docker_credentials: "DockerCredentials",
    follow: bool = False,
    stdout: bool = False,
    stderr: bool = False,
    since: int = 0,
    until: int = 0,
    timestamps: bool = False,
    tail: str = "all",
) -> Dict[str, Any]:
    """
    Get `stdout` and `stderr` logs from a container.  Note: This endpoint works only
    for containers with the `json-file` or `journald` logging driver.

    Args:
        id:
            Id used in formatting the endpoint URL.
        docker_credentials:
            Credentials to use for authentication with Docker.
        follow:
            Keep connection after returning logs.
        stdout:
            Return logs from `stdout`.
        stderr:
            Return logs from `stderr`.
        since:
            Only return logs since this time, as a UNIX timestamp.
        until:
            Only return logs before this time, as a UNIX timestamp.
        timestamps:
            Add timestamps to every log line.
        tail:
            Only return this number of log lines from the end of the logs. Specify
            as an integer or `all` to output all log lines.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/containers/{id}/logs`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | logs returned as a stream in response body. For the stream format, [see the    documentation for the attach endpoint](    operation/ContainerAttach). Note that unlike the attach endpoint, the logs    endpoint does not upgrade the connection and does not set Content-Type. |
    | 404 | no such container. |
    | 500 | server error. |
    """  # noqa
    endpoint = f"/containers/{id}/logs"  # noqa
    responses = {
        200: (  # noqa
            "logs returned as a stream in response body. For the stream format, [see"
            " the    documentation for the attach endpoint](   "
            " operation/ContainerAttach). Note that unlike the attach endpoint, the"
            " logs    endpoint does not upgrade the connection and does not set"
            " Content-Type."
        ),
        404: "no such container.",  # noqa
        500: "server error.",  # noqa
    }

    params = {
        "id": id,
        "follow": follow,
        "stdout": stdout,
        "stderr": stderr,
        "since": since,
        "until": until,
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


@task
async def container_changes(
    id: str,
    docker_credentials: "DockerCredentials",
) -> Dict[str, Any]:
    """
    Returns which files in a container's filesystem have been added, deleted, or
    modified. The `Kind` of modification can be one of:  - `0`: Modified - `1`:
    Added - `2`: Deleted.

    Args:
        id:
            Id used in formatting the endpoint URL.
        docker_credentials:
            Credentials to use for authentication with Docker.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/containers/{id}/changes`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | The list of changes. |
    | 404 | no such container. |
    | 500 | server error. |
    """  # noqa
    endpoint = f"/containers/{id}/changes"  # noqa
    responses = {
        200: "The list of changes.",  # noqa
        404: "no such container.",  # noqa
        500: "server error.",  # noqa
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
async def container_export(
    id: str,
    docker_credentials: "DockerCredentials",
) -> Dict[str, Any]:
    """
    Export the contents of a container as a tarball.

    Args:
        id:
            Id used in formatting the endpoint URL.
        docker_credentials:
            Credentials to use for authentication with Docker.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/containers/{id}/export`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | no error. |
    | 404 | no such container. |
    | 500 | server error. |
    """  # noqa
    endpoint = f"/containers/{id}/export"  # noqa
    responses = {
        200: "no error.",  # noqa
        404: "no such container.",  # noqa
        500: "server error.",  # noqa
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
async def container_stats(
    id: str,
    docker_credentials: "DockerCredentials",
    stream: bool = True,
    one_shot: bool = False,
) -> Dict[str, Any]:
    """
    This endpoint returns a live stream of a container’s resource usage statistics.
    The `precpu_stats` is the CPU statistic of the *previous* read, and is used
    to calculate the CPU usage percentage. It is not an exact copy of the
    `cpu_stats` field.  If either `precpu_stats.online_cpus` or
    `cpu_stats.online_cpus` is nil then for compatibility with older daemons the
    length of the corresponding `cpu_usage.percpu_usage` array should be used.
    On a cgroup v2 host, the following fields are not set * `blkio_stats`: all
    fields other than `io_service_bytes_recursive` * `cpu_stats`:
    `cpu_usage.percpu_usage` * `memory_stats`: `max_usage` and `failcnt` Also,
    `memory_stats.stats` fields are incompatible with cgroup v1.  To calculate
    the values shown by the `stats` command of the docker cli tool the following
    formulas can be used: * used_memory = `memory_stats.usage -
    memory_stats.stats.cache` * available_memory = `memory_stats.limit` * Memory
    usage % = `(used_memory / available_memory) * 100.0` * cpu_delta =
    `cpu_stats.cpu_usage.total_usage - precpu_stats.cpu_usage.total_usage` *
    system_cpu_delta = `cpu_stats.system_cpu_usage -
    precpu_stats.system_cpu_usage` * number_cpus =
    `lenght(cpu_stats.cpu_usage.percpu_usage)` or `cpu_stats.online_cpus` * CPU
    usage % = `(cpu_delta / system_cpu_delta) * number_cpus * 100.0`.

    Args:
        id:
            Id used in formatting the endpoint URL.
        docker_credentials:
            Credentials to use for authentication with Docker.
        stream:
            Stream the output. If false, the stats will be output once and then it
            will disconnect.
        one_shot:
            Only get a single stat instead of waiting for 2 cycles. Must be used
            with `stream=false`.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/containers/{id}/stats`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | no error. |
    | 404 | no such container. |
    | 500 | server error. |
    """  # noqa
    endpoint = f"/containers/{id}/stats"  # noqa
    responses = {
        200: "no error.",  # noqa
        404: "no such container.",  # noqa
        500: "server error.",  # noqa
    }

    params = {
        "id": id,
        "stream": stream,
        "one_shot": one_shot,
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
async def container_resize(
    id: str,
    docker_credentials: "DockerCredentials",
    h: int = None,
    w: int = None,
) -> Dict[str, Any]:
    """
    Resize the TTY for a container.

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
    `/containers/{id}/resize`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | no error. |
    | 404 | no such container. |
    | 500 | cannot resize container. |
    """  # noqa
    endpoint = f"/containers/{id}/resize"  # noqa
    responses = {
        200: "no error.",  # noqa
        404: "no such container.",  # noqa
        500: "cannot resize container.",  # noqa
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
async def container_start(
    id: str,
    docker_credentials: "DockerCredentials",
    detach_keys: str = None,
) -> Dict[str, Any]:
    """
    Start a container.

    Args:
        id:
            Id used in formatting the endpoint URL.
        docker_credentials:
            Credentials to use for authentication with Docker.
        detach_keys:
            Override the key sequence for detaching a container. Format is a single
            character `[a-Z]` or `ctrl-<value>` where `<value>` is one
            of: `a-z`, `@`, `^`, `[`, `,` or `_`.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/containers/{id}/start`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 204 | no error. |
    | 304 | container already started. |
    | 404 | no such container. |
    | 500 | server error. |
    """  # noqa
    endpoint = f"/containers/{id}/start"  # noqa
    responses = {
        204: "no error.",  # noqa
        304: "container already started.",  # noqa
        404: "no such container.",  # noqa
        500: "server error.",  # noqa
    }

    params = {
        "id": id,
        "detach_keys": detach_keys,
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
async def container_stop(
    id: str,
    docker_credentials: "DockerCredentials",
    t: int = None,
) -> Dict[str, Any]:
    """
    Stop a container.

    Args:
        id:
            Id used in formatting the endpoint URL.
        docker_credentials:
            Credentials to use for authentication with Docker.
        t:
            Number of seconds to wait before killing the container.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/containers/{id}/stop`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 204 | no error. |
    | 304 | container already stopped. |
    | 404 | no such container. |
    | 500 | server error. |
    """  # noqa
    endpoint = f"/containers/{id}/stop"  # noqa
    responses = {
        204: "no error.",  # noqa
        304: "container already stopped.",  # noqa
        404: "no such container.",  # noqa
        500: "server error.",  # noqa
    }

    params = {
        "id": id,
        "t": t,
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
async def container_restart(
    id: str,
    docker_credentials: "DockerCredentials",
    t: int = None,
) -> Dict[str, Any]:
    """
    Restart a container.

    Args:
        id:
            Id used in formatting the endpoint URL.
        docker_credentials:
            Credentials to use for authentication with Docker.
        t:
            Number of seconds to wait before killing the container.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/containers/{id}/restart`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 204 | no error. |
    | 404 | no such container. |
    | 500 | server error. |
    """  # noqa
    endpoint = f"/containers/{id}/restart"  # noqa
    responses = {
        204: "no error.",  # noqa
        404: "no such container.",  # noqa
        500: "server error.",  # noqa
    }

    params = {
        "id": id,
        "t": t,
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
async def container_kill(
    id: str,
    docker_credentials: "DockerCredentials",
    signal: str = "SIGKILL",
) -> Dict[str, Any]:
    """
    Send a POSIX signal to a container, defaulting to killing to the container.

    Args:
        id:
            Id used in formatting the endpoint URL.
        docker_credentials:
            Credentials to use for authentication with Docker.
        signal:
            Signal to send to the container as an integer or string (e.g. `SIGINT`).

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/containers/{id}/kill`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 204 | no error. |
    | 404 | no such container. |
    | 409 | container is not running. |
    | 500 | server error. |
    """  # noqa
    endpoint = f"/containers/{id}/kill"  # noqa
    responses = {
        204: "no error.",  # noqa
        404: "no such container.",  # noqa
        409: "container is not running.",  # noqa
        500: "server error.",  # noqa
    }

    params = {
        "id": id,
        "signal": signal,
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
async def container_update(
    id: str,
    update: str,
    docker_credentials: "DockerCredentials",
) -> Dict[str, Any]:
    """
    Change various configuration options of a container without having to recreate
    it.

    Args:
        id:
            Id used in formatting the endpoint URL.
        update:

        docker_credentials:
            Credentials to use for authentication with Docker.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/containers/{id}/update`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | The container has been updated. |
    | 404 | no such container. |
    | 500 | server error. |
    """  # noqa
    endpoint = f"/containers/{id}/update"  # noqa
    responses = {
        200: "The container has been updated.",  # noqa
        404: "no such container.",  # noqa
        500: "server error.",  # noqa
    }

    params = {
        "id": id,
        "update": update,
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
async def container_rename(
    id: str,
    name: str,
    docker_credentials: "DockerCredentials",
) -> Dict[str, Any]:
    """
    Rename a container.

    Args:
        id:
            Id used in formatting the endpoint URL.
        name:
            New name for the container.
        docker_credentials:
            Credentials to use for authentication with Docker.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/containers/{id}/rename`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 204 | no error. |
    | 404 | no such container. |
    | 409 | name already in use. |
    | 500 | server error. |
    """  # noqa
    endpoint = f"/containers/{id}/rename"  # noqa
    responses = {
        204: "no error.",  # noqa
        404: "no such container.",  # noqa
        409: "name already in use.",  # noqa
        500: "server error.",  # noqa
    }

    params = {
        "id": id,
        "name": name,
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
async def container_pause(
    id: str,
    docker_credentials: "DockerCredentials",
) -> Dict[str, Any]:
    """
    Use the freezer cgroup to suspend all processes in a container.  Traditionally,
    when suspending a process the `SIGSTOP` signal is used, which is observable
    by the process being suspended. With the freezer cgroup the process is
    unaware, and unable to capture, that it is being suspended, and subsequently
    resumed.

    Args:
        id:
            Id used in formatting the endpoint URL.
        docker_credentials:
            Credentials to use for authentication with Docker.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/containers/{id}/pause`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 204 | no error. |
    | 404 | no such container. |
    | 500 | server error. |
    """  # noqa
    endpoint = f"/containers/{id}/pause"  # noqa
    responses = {
        204: "no error.",  # noqa
        404: "no such container.",  # noqa
        500: "server error.",  # noqa
    }

    params = {
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
async def container_unpause(
    id: str,
    docker_credentials: "DockerCredentials",
) -> Dict[str, Any]:
    """
    Resume a container which has been paused.

    Args:
        id:
            Id used in formatting the endpoint URL.
        docker_credentials:
            Credentials to use for authentication with Docker.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/containers/{id}/unpause`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 204 | no error. |
    | 404 | no such container. |
    | 500 | server error. |
    """  # noqa
    endpoint = f"/containers/{id}/unpause"  # noqa
    responses = {
        204: "no error.",  # noqa
        404: "no such container.",  # noqa
        500: "server error.",  # noqa
    }

    params = {
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
async def container_attach(
    id: str,
    docker_credentials: "DockerCredentials",
    detach_keys: str = None,
    logs: bool = False,
    stream: bool = False,
    stdin: bool = False,
    stdout: bool = False,
    stderr: bool = False,
) -> Dict[str, Any]:
    """
    Attach to a container to read its output or send it input. You can attach to the
    same container multiple times and you can reattach to containers that have
    been detached.  Either the `stream` or `logs` parameter must be `true` for
    this endpoint to do anything.  See the [documentation for the `docker
    attach` command](/engine/reference/commandline/attach/) for more details.
    Hijacking  This endpoint hijacks the HTTP connection to transport `stdin`,
    `stdout`, and `stderr` on the same socket.  This is the response from the
    daemon for an attach request:  ``` HTTP/1.1 200 OK Content-Type:
    application/vnd.docker.raw-stream  [STREAM] ```  After the headers and two
    new lines, the TCP connection can now be used for raw, bidirectional
    communication between the client and server.  To hint potential proxies
    about connection hijacking, the Docker client can also optionally send
    connection upgrade headers.  For example, the client sends this request to
    upgrade the connection:  ``` POST
    /containers/16253994b7c4/attach?stream=1&stdout=1 HTTP/1.1 Upgrade: tcp
    Connection: Upgrade ```  The Docker daemon will respond with a `101
    UPGRADED` response, and will similarly follow with the raw stream:  ```
    HTTP/1.1 101 UPGRADED Content-Type: application/vnd.docker.raw-stream
    Connection: Upgrade Upgrade: tcp  [STREAM] ```
    Stream format  When the TTY setting is disabled in [`POST
    /containers/create`](
    operation/ContainerCreate), the stream over the hijacked connected is
    multiplexed to separate out `stdout` and `stderr`. The stream consists of a
    series of frames, each containing a header and a payload.  The header
    contains the information which the stream writes (`stdout` or `stderr`). It
    also contains the size of the associated frame encoded in the last four
    bytes (`uint32`).  It is encoded on the first eight bytes like this:  ```go
    header := [8]byte{STREAM_TYPE, 0, 0, 0, SIZE1, SIZE2, SIZE3, SIZE4} ```
    `STREAM_TYPE` can be:  - 0: `stdin` (is written on `stdout`) - 1: `stdout` -
    2: `stderr`  `SIZE1, SIZE2, SIZE3, SIZE4` are the four bytes of the `uint32`
    size encoded as big endian.  Following the header is the payload, which is
    the specified number of bytes of `STREAM_TYPE`.  The simplest way to
    implement this protocol is the following:  1. Read 8 bytes. 2. Choose
    `stdout` or `stderr` depending on the first byte. 3. Extract the frame size
    from the last four bytes. 4. Read the extracted size and output it on the
    correct output. 5. Goto 1.
    Stream format when using a TTY  When the TTY setting is enabled in [`POST
    /containers/create`](
    operation/ContainerCreate), the stream is not multiplexed. The data
    exchanged over the hijacked connection is simply the raw data from the
    process PTY and client's `stdin`.

    Args:
        id:
            Id used in formatting the endpoint URL.
        docker_credentials:
            Credentials to use for authentication with Docker.
        detach_keys:
            Override the key sequence for detaching a container.Format is a single
            character `[a-Z]` or `ctrl-<value>` where `<value>` is one
            of: `a-z`, `@`, `^`, `[`, `,` or `_`.
        logs:
            Replay previous logs from the container.  This is useful for attaching
            to a container that has started and you want to output
            everything since the container started.  If `stream` is also
            enabled, once all the previous output has been returned, it
            will seamlessly transition into streaming current output.
        stream:
            Stream attached streams from the time the request was made onwards.
        stdin:
            Attach to `stdin`.
        stdout:
            Attach to `stdout`.
        stderr:
            Attach to `stderr`.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/containers/{id}/attach`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 101 | no error, hints proxy about hijacking. |
    | 200 | no error, no upgrade header found. |
    | 400 | bad parameter. |
    | 404 | no such container. |
    | 500 | server error. |
    """  # noqa
    endpoint = f"/containers/{id}/attach"  # noqa
    responses = {
        101: "no error, hints proxy about hijacking.",  # noqa
        200: "no error, no upgrade header found.",  # noqa
        400: "bad parameter.",  # noqa
        404: "no such container.",  # noqa
        500: "server error.",  # noqa
    }

    params = {
        "id": id,
        "detach_keys": detach_keys,
        "logs": logs,
        "stream": stream,
        "stdin": stdin,
        "stdout": stdout,
        "stderr": stderr,
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
async def container_attach_websocket(
    id: str,
    docker_credentials: "DockerCredentials",
    detach_keys: str = None,
    logs: bool = False,
    stream: bool = False,
) -> Dict[str, Any]:
    """
    Attach to a container via a websocket.

    Args:
        id:
            Id used in formatting the endpoint URL.
        docker_credentials:
            Credentials to use for authentication with Docker.
        detach_keys:
            Override the key sequence for detaching a container.Format is a single
            character `[a-Z]` or `ctrl-<value>` where `<value>` is one
            of: `a-z`, `@`, `^`, `[`, `,`, or `_`.
        logs:
            Return logs.
        stream:
            Return stream.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/containers/{id}/attach/ws`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 101 | no error, hints proxy about hijacking. |
    | 200 | no error, no upgrade header found. |
    | 400 | bad parameter. |
    | 404 | no such container. |
    | 500 | server error. |
    """  # noqa
    endpoint = f"/containers/{id}/attach/ws"  # noqa
    responses = {
        101: "no error, hints proxy about hijacking.",  # noqa
        200: "no error, no upgrade header found.",  # noqa
        400: "bad parameter.",  # noqa
        404: "no such container.",  # noqa
        500: "server error.",  # noqa
    }

    params = {
        "id": id,
        "detach_keys": detach_keys,
        "logs": logs,
        "stream": stream,
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
async def container_wait(
    id: str,
    docker_credentials: "DockerCredentials",
    condition: str = "not-running",
) -> Dict[str, Any]:
    """
    Block until a container stops, then returns the exit code.

    Args:
        id:
            Id used in formatting the endpoint URL.
        docker_credentials:
            Credentials to use for authentication with Docker.
        condition:
            Wait until a container state reaches the given condition.  Defaults to
            `not-running` if omitted or empty.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/containers/{id}/wait`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | The container has exit. |
    | 400 | bad parameter. |
    | 404 | no such container. |
    | 500 | server error. |
    """  # noqa
    endpoint = f"/containers/{id}/wait"  # noqa
    responses = {
        200: "The container has exit.",  # noqa
        400: "bad parameter.",  # noqa
        404: "no such container.",  # noqa
        500: "server error.",  # noqa
    }

    params = {
        "id": id,
        "condition": condition,
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
async def container_delete(
    id: str,
    docker_credentials: "DockerCredentials",
    v: bool = False,
    force: bool = False,
    link: bool = False,
) -> Dict[str, Any]:
    """
    Remove a container.

    Args:
        id:
            Id used in formatting the endpoint URL.
        docker_credentials:
            Credentials to use for authentication with Docker.
        v:
            Remove anonymous volumes associated with the container.
        force:
            If the container is running, kill it before removing it.
        link:
            Remove the specified link associated with the container.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/containers/{id}`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 204 | no error. |
    | 400 | bad parameter. |
    | 404 | no such container. |
    | 409 | conflict. |
    | 500 | server error. |
    """  # noqa
    endpoint = f"/containers/{id}"  # noqa
    responses = {
        204: "no error.",  # noqa
        400: "bad parameter.",  # noqa
        404: "no such container.",  # noqa
        409: "conflict.",  # noqa
        500: "server error.",  # noqa
    }

    params = {
        "id": id,
        "v": v,
        "force": force,
        "link": link,
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
async def container_archive(
    id: str,
    path: str,
    docker_credentials: "DockerCredentials",
) -> Dict[str, Any]:
    """
    Get a tar archive of a resource in the filesystem of container id.

    Args:
        id:
            Id used in formatting the endpoint URL.
        path:
            Resource in the container’s filesystem to archive.
        docker_credentials:
            Credentials to use for authentication with Docker.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/containers/{id}/archive`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | no error. |
    | 400 | Bad parameter. |
    | 404 | Container or path does not exist. |
    | 500 | server error. |
    """  # noqa
    endpoint = f"/containers/{id}/archive"  # noqa
    responses = {
        200: "no error.",  # noqa
        400: "Bad parameter.",  # noqa
        404: "Container or path does not exist.",  # noqa
        500: "server error.",  # noqa
    }

    params = {
        "id": id,
        "path": path,
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
async def put_container_archive(
    id: str,
    path: str,
    input_stream: str,
    docker_credentials: "DockerCredentials",
    no_overwrite_dir_non_dir: str = None,
    copy_uidgid: str = None,
) -> Dict[str, Any]:
    """
    Upload a tar archive to be extracted to a path in the filesystem of container
    id. `path` parameter is asserted to be a directory. If it exists as a file,
    400 error will be returned with message 'not a directory'.

    Args:
        id:
            Id used in formatting the endpoint URL.
        path:
            Path to a directory in the container to extract the archive’s contents
            into.
        input_stream:
            The input stream must be a tar archive compressed with one of the
            following algorithms: `identity` (no compression), `gzip`,
            `bzip2`, or `xz`.
        docker_credentials:
            Credentials to use for authentication with Docker.
        no_overwrite_dir_non_dir:
            If `1`, `true`, or `True` then it will be an error if unpacking the
            given content would cause an existing directory to be
            replaced with a non-directory and vice versa.
        copy_uidgid:
            If `1`, `true`, then it will copy UID/GID maps to the dest file or dir.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/containers/{id}/archive`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | The content was extracted successfully. |
    | 400 | Bad parameter. |
    | 403 | Permission denied, the volume or container rootfs is marked as read-only. |
    | 404 | No such container or path does not exist inside the container. |
    | 500 | Server error. |
    """  # noqa
    endpoint = f"/containers/{id}/archive"  # noqa
    responses = {
        200: "The content was extracted successfully.",  # noqa
        400: "Bad parameter.",  # noqa
        403: (  # noqa
            "Permission denied, the volume or container rootfs is marked as read-only."
        ),
        404: "No such container or path does not exist inside the container.",  # noqa
        500: "Server error.",  # noqa
    }

    params = {
        "id": id,
        "path": path,
        "no_overwrite_dir_non_dir": no_overwrite_dir_non_dir,
        "copy_uidgid": copy_uidgid,
        "input_stream": input_stream,
    }

    response = await execute_endpoint.fn(
        endpoint,
        docker_credentials,
        http_method=HTTPMethod.PUT,
        params=params,
    )

    contents = _unpack_contents(response, responses)
    return contents


@task
async def container_prune(
    docker_credentials: "DockerCredentials",
    filters: str = None,
) -> Dict[str, Any]:
    """
    Delete stopped containers.

    Args:
        docker_credentials:
            Credentials to use for authentication with Docker.
        filters:
            Filters to process on the prune list, encoded as JSON (a
            `map[string][]string`).  Available filters: -
            `until=<timestamp>` Prune containers created before this
            timestamp. The `<timestamp>` can be Unix timestamps, date
            formatted timestamps, or Go duration strings (e.g. `10m`,
            `1h30m`) computed relative to the daemon machine’s time. -
            `label` (`label=<key>`, `label=<key>=<value>`,
            `label!=<key>`, or `label!=<key>=<value>`) Prune containers
            with (or without, in case `label!=...` is used) the
            specified labels.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/containers/prune`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | No error. |
    | 500 | Server error. |
    """  # noqa
    endpoint = "/containers/prune"  # noqa

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


@task
async def container_exec(
    exec_config: Dict,
    id: str,
    docker_credentials: "DockerCredentials",
) -> Dict[str, Any]:
    """
    Run a command inside a running container.

    Args:
        exec_config:
            Exec configuration.
        id:
            Id used in formatting the endpoint URL.
        docker_credentials:
            Credentials to use for authentication with Docker.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/containers/{id}/exec`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 201 | no error. |
    | 404 | no such container. |
    | 409 | container is paused. |
    | 500 | Server error. |
    """  # noqa
    endpoint = f"/containers/{id}/exec"  # noqa
    responses = {
        201: "no error.",  # noqa
        404: "no such container.",  # noqa
        409: "container is paused.",  # noqa
        500: "Server error.",  # noqa
    }

    params = {
        "exec_config": exec_config,
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
