#
#    Copyright 2019 EPAM Systems
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
"""
Docker image builder
"""
import json
import logging
import os
import typing

import docker
from odahuflow.sdk.models import Connection

from odahuflow.packager.helpers.extensions.ecr import ECR_CONNECTION_TYPE, get_ecr_credentials
from odahuflow.packager.helpers.io_proc_utils import run

BUILDAH_BIN = os.getenv('BUILDAH_BIN', 'buildah')
LOGGER = logging.getLogger(__name__)


def extract_docker_login_credentials(
        connection: Connection,
        docker_image_url: typing.Optional[str] = None) -> typing.Tuple[str, str, str]:
    """
    Extract docker login credentials from connection

    :param docker_image_url:
    :param connection: connection
    :return: registry, login, password
    """
    if connection.spec.type == ECR_CONNECTION_TYPE and docker_image_url:
        user, password = get_ecr_credentials(connection.spec, docker_image_url)
        logging.info("ECR credentials were generated")

        return connection.spec.uri, user, password

    logging.info(
        f"For connection type {connection.spec.type} and docker image {docker_image_url} "
        f"credentials from connection were returned"
    )
    return connection.spec.uri, connection.spec.username, connection.spec.password


def test_is_docker_available() -> None:
    """
    Check is docker socket available

    :return: is buildah available
    """
    return os.path.exists("/var/run/docker.sock")


def _extract_buildah_credentials(connection: typing.Optional[Connection] = None,
                                 docker_image_url: typing.Optional[str] = None) -> typing.List[str]:
    """
    Extract argument for buildah

    :param connection: connection
    :return: typing.List[str]
    """
    if not connection:
        return []

    _, login, password = extract_docker_login_credentials(connection, docker_image_url)

    logging.info('Using password %r for user %r',
                 '*' * len(password), login)

    return [
        '--creds',
        f'{login}:{password}'
    ]


def build_docker_image_buildah(context,
                               docker_file,
                               external_docker_name,
                               pull_connection: typing.Optional[Connection] = None):
    """
    Build the docker image using buildah

    :param context: docker build context
    :param docker_file: Dockerfile name (relative to docker build context)
    :param external_docker_name: external docker image target name, without host
    :param pull_connection: connection for pulling Docker image during build from
    """
    logging.info('Starting building of new image')

    build_args = [
        BUILDAH_BIN, 'build-using-dockerfile',
        *_extract_buildah_credentials(pull_connection),
        '--device', '/dev/fuse:rw',
        '--file', docker_file,
        '--format', 'docker',
        '--compress',
        '--tag', external_docker_name,
        context
    ]
    run(*build_args)


def push_docker_image_buildah(external_docker_name, push_connection: typing.Optional[Connection]) -> str:
    """
    Push the docker image using buildah

    :param external_docker_name: external docker image target name, without host
    :param push_connection: connection for pushing Docker images to
    """
    if not push_connection:
        return external_docker_name

    remote_tag = f'{push_connection.spec.uri}/{external_docker_name}'

    logging.info('Starting pushing of image')
    tag_args = [
        BUILDAH_BIN, 'tag',
        external_docker_name,
        remote_tag
    ]
    run(*tag_args)

    logging.info('Starting pushing of image')
    push_args = [
        BUILDAH_BIN, 'push',
        *_extract_buildah_credentials(push_connection, remote_tag),
        remote_tag
    ]
    run(*push_args, sensitive=True)

    return remote_tag


def _authorize_docker(client: docker.DockerClient, connection: Connection,
                      docker_image_url: typing.Optional[str] = None):
    """
    Authorize docker api on external registry

    :param client: docker API
    :type client: docker.DockerClient
    :param connection: connection credentials
    :return: None
    """
    registry, login, password = extract_docker_login_credentials(connection, docker_image_url)

    logging.info('Trying to authorize %r on %r using password %r',
                 login, registry,
                 '*' * len(connection.spec.password))
    client.login(username=login,
                 password=password,
                 registry=registry,
                 reauth=True)


def build_docker_image_docker(context,
                              docker_file,
                              external_docker_name,
                              pull_connection: typing.Optional[Connection] = None):
    """
    Build the docker image using docker

    :param context: docker build context
    :param docker_file: Dockerfile name (relative to docker build context)
    :param external_docker_name: external docker image target name, without host
    :param pull_connection: (Optional) connection for pulling Docker image during build from
    """
    logging.debug('Building docker client from ENV variables')
    client = docker.from_env()
    # Authorize for pull
    if pull_connection:
        logging.debug('Trying to authorize user fo pulling sources')
        _authorize_docker(client, pull_connection)

    # Build image
    streamer = client.api.build(path=context,
                                rm=True,
                                dockerfile=docker_file,
                                tag=external_docker_name)

    for chunk in streamer:
        if isinstance(chunk, bytes):
            chunk = chunk.decode('utf-8')

        try:
            chunk_json = json.loads(chunk)
            if 'error' in chunk_json:
                raise Exception(chunk_json['error'])
            if 'stream' in chunk_json:
                for line in chunk_json['stream'].splitlines():
                    LOGGER.info(line.strip())

        except json.JSONDecodeError:
            LOGGER.info(chunk)


def push_docker_image_docker(external_docker_name, push_connection: typing.Optional[Connection]) -> str:
    """
    Push the docker image using docker

    :param external_docker_name: external docker image target name, without host
    :param push_connection: connection for pushing Docker images to
    """
    logging.debug('Building docker client from ENV variables')
    client = docker.from_env()

    if not push_connection:
        # Tag local image
        local_built = client.images.get(external_docker_name)
        local_built.tag(external_docker_name)

        return external_docker_name

    remote_tag = f'{push_connection.spec.uri}/{external_docker_name}'
    local_built = client.images.get(external_docker_name)
    local_built.tag(remote_tag)

    logging.debug('Trying to authorize user to push result image')
    _authorize_docker(client, push_connection, remote_tag)

    log_generator = client.images.push(
        repository=remote_tag,
        stream=True,
        auth_config={
            'username': push_connection.spec.username,
            'password': push_connection.spec.password
        }
    )

    for line in log_generator:
        if isinstance(line, bytes):
            line = line.decode('utf-8')

        LOGGER.info(line)

    client.images.remove(remote_tag)
    client.images.remove(external_docker_name)

    return remote_tag


def build_docker_image(context,
                       docker_file,
                       external_docker_name,
                       pull_connection: typing.Optional[Connection] = None):
    """
    Build and push docker image

    :param context: docker build context (folder name)
    :param docker_file: Dockerfile name (relative to docker build context)
    :param external_docker_name: external docker image target name, without host
    :param pull_connection: (Optional) connection for pulling Docker image during build from
    """
    if test_is_docker_available():
        build_docker_image_docker(context, docker_file, external_docker_name, pull_connection)
    else:
        build_docker_image_buildah(context, docker_file, external_docker_name, pull_connection)


def push_docker_image(external_docker_name: str, push_connection: Connection) -> str:
    """
    Push docker image

    :param external_docker_name: external docker image target name, without host
    :param push_connection: connection for pushing Docker images to
    """
    if test_is_docker_available():
        return push_docker_image_docker(external_docker_name, push_connection)
    else:
        return push_docker_image_buildah(external_docker_name, push_connection)
