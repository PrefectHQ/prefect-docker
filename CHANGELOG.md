# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security

## 0.3.3

### Added
- allow multiple Docker tags for build and push steps

## 0.3.2

Released July 20th, 2023.

### Changed
- Promoted workers to GA, removed beta disclaimers

## 0.3.1

Released June 26th, 2023.

### Fixed

- Fix requirements installation when using `build_docker_image` step with `dockerfile='auto'` - [#68](https://github.com/PrefectHQ/prefect-docker/pull/68)

## 0.3.0

Released June 15th, 2023.

Note this release contains a breaking change to the `build_docker_image` step. The `image_name` output key has been changed to only include the image name and not the image tag. The `image` output key now contains the image name and image tag and can be used in situations where `image_name` was previously used.

If you were previously using `build_docker_image` in your `prefect.yaml` or `deployment.yaml` file, you'll need to update your `image_name` references.

For example, if you were using `image_name` in your work pool job variables:

``` yaml
work_pool:
  name: my-work-pool
  job_variables:
    image: "{{ image_name }}"
```

you'll need to use `image` instead:

```yaml
work_pool:
  name: my-work-pool
  job_variables:
    image: "{{ image }}"
```

Alternatively, you can put an upper version limit on the version of `prefect-docker` used for `build_docker_image` in your `prefect.yaml` file:

```yaml
build:
- prefect_docker.projects.steps.build_docker_image:
    id: build_image
    requires: prefect-docker>=0.2.0<0.3.0
    image_name: my-image
    tag: my-tag
    dockerfile: auto
    push: true
```

### Added

- Emit a Prefect event when creation of a docker container fails - [#50](https://github.com/PrefectHQ/prefect-docker/pull/50)
- Ability to pass build kwargs into `build_docker_image` - [#51](https://github.com/PrefectHQ/prefect-docker/pull/51)
- `image_id` and `image` to `build_docker_image` output. image has the same contents as the current `image_name` - [#51](https://github.com/PrefectHQ/prefect-docker/pull/51)
- `push_docker_image` step - [#64](https://github.com/PrefectHQ/prefect-docker/pull/64)

### Changed

- BREAKING: `image_name` updated to contain only the image name without the tag - [#51](https://github.com/PrefectHQ/prefect-docker/pull/51)

### Deprecated

- `prefect_docker.projects` module. Use `prefect_docker.deployments` instead. - [#63](https://github.com/PrefectHQ/prefect-docker/pull/63)
- `push` on `build_docker_image`. Use `push_docker_image` instead. - [#64](https://github.com/PrefectHQ/prefect-docker/pull/64)


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
