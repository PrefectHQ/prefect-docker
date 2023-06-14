# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added

- Emit a Prefect event when creation of a docker container fails.
- Ability to pass build kwargs into `build_docker_image` - [#51](https://github.com/PrefectHQ/prefect-docker/pull/51)
- `image_id` and `image` to `build_docker_image` output. image has the same contents as the current `image_name` - [#51](https://github.com/PrefectHQ/prefect-docker/pull/51)
- `push_docker_image` step - [#64](https://github.com/PrefectHQ/prefect-docker/pull/64)

### Changed

- BREAKING: `image_name` updated to contain only the image name without the tag - [#51](https://github.com/PrefectHQ/prefect-docker/pull/51)

### Deprecated

- `prefect_docker.projects` module. Use `prefect_docker.deployments` instead. - [#63](https://github.com/PrefectHQ/prefect-docker/pull/63)
- `push` on `build_docker_image`. Use `push_docker_image` instead. - [#64](https://github.com/PrefectHQ/prefect-docker/pull/64)

### Removed

### Fixed

### Security

## 0.2.2

Released April 20th, 2023.

### Added

- `kill_infrastructure` method on `DockerWorker` which stops containers for cancelled flow runs  - [#48](https://github.com/PrefectHQ/prefect-docker/pull/48)

## 0.2.1

Released April 6th, 2023.

### Added

- Error out on worker start if using ephemeral API - [#45](https://github.com/PrefectHQ/prefect-docker/pull/35)

## 0.2.0

Released April 6th, 2023.

### Added

- Beta `DockerWorker` for executing flow runs within Docker containers - [#35](https://github.com/PrefectHQ/prefect-docker/pull/35)
- Beta 'docker_build_image' project step for building Docker images prior to creating a deployment - [#38](https://github.com/PrefectHQ/prefect-docker/pull/38)

### Fixed

- correct type hints for tasks - [#31](https://github.com/PrefectHQ/prefect-docker/issues/31)

## 0.1.0

Released on October 21st, 2022.

### Added

- `DockerHost` block - [#3](https://github.com/PrefectHQ/prefect-docker/pull/3) and [#13](https://github.com/PrefectHQ/prefect-docker/pull/13)
- `pull_docker_image` task - [#9](https://github.com/PrefectHQ/prefect-docker/pull/9)
- `create_docker_container` task - [#12](https://github.com/PrefectHQ/prefect-docker/pull/12)
- `get_docker_container_logs` task - [#14](https://github.com/PrefectHQ/prefect-docker/pull/14)
- `start_docker_container` task - [#18](https://github.com/PrefectHQ/prefect-docker/pull/18)
- `stop_docker_container` task - [#24](https://github.com/PrefectHQ/prefect-docker/pull/24)
- `remove_docker_container` task - [#25](https://github.com/PrefectHQ/prefect-docker/pull/25)
