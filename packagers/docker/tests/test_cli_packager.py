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
# pylint: disable=redefined-outer-name
import json
import logging
import os
import tempfile
from typing import List
from unittest import mock

import docker
import pytest
from docker.models.images import ImageCollection
from odahuflow.packager.cli import work_resource_file
from odahuflow.packager.helpers.io_proc_utils import run
from odahuflow.sdk.models import K8sPackager, ModelPackaging, ModelPackagingSpec, PackagingIntegration, \
    PackagingIntegrationSpec, Schema, JsonSchema, PackagerTarget, Connection, ConnectionSpec

RESOURCES_DIR = f'{os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources")}'
LEN_REMOVED_IMAGES_REPR = 'two images must be deleted from local machine: local and for external registry'

patch_obj = mock.patch.object


@pytest.fixture()
def packager_manifest_file() -> str:
    """
    Returns path to a temporary Packager file
    """
    with tempfile.NamedTemporaryFile(mode="w") as temp_file:
        temp_file.write(json.dumps(
            K8sPackager(
                model_packaging=ModelPackaging(
                    id="wine",
                    spec=ModelPackagingSpec(
                        integration_name="docker-cli",
                        targets=[],
                    ),
                ),
                packaging_integration=PackagingIntegration(
                    id="docker-cli",
                    spec=PackagingIntegrationSpec(
                        schema=Schema(
                            arguments=JsonSchema(
                                properties=[],
                            )
                        )
                    )
                ),
                targets=[
                    PackagerTarget(
                        name="docker-push",
                        connection=Connection(
                            id="docker-ci",
                            spec=ConnectionSpec(
                                type="docker",
                                uri="gcr.io/some-url",
                                username="username",
                                password="password",
                            ),
                        ),
                    ),
                ],
            ).to_dict()
        ))
        temp_file.flush()

        yield temp_file.name


class MockImageRemover:
    """
    Instead of calling docker client remove api for deleting image just remember image name
    was
    """

    def __init__(self):
        self.images_for_removing: List[str] = []

    def __call__(self, image_name: str, *args, **kwargs):
        self.images_for_removing.append(image_name)


def mock_push(*args, **kwargs):
    yield  # init generator
    yield 'Image is not pushed because of mocking'


def test_cli(tmp_path, packager_manifest_file: str):
    logging.basicConfig(level=logging.DEBUG)

    model_path = os.path.join(RESOURCES_DIR, 'simple-model')

    image_remover = MockImageRemover()

    try:
        with patch_obj(ImageCollection, 'remove', image_remover), patch_obj(ImageCollection, 'push', mock_push):
            # pylint: disable=unexpected-keyword-arg,no-value-for-parameter
            work_resource_file([model_path, packager_manifest_file, '--verbose'], standalone_mode=False)

        assert len(image_remover.images_for_removing) == 2, LEN_REMOVED_IMAGES_REPR

        any_image = image_remover.images_for_removing[0]

        input_fp = os.path.join(tmp_path, 'input.json')
        output_fp = os.path.join(tmp_path, 'results.json')

        with open(input_fp, 'w') as f:
            json.dump({
                'columns': 'Destiny line',
                'data': [[1, 2, 3, 4]]
            }, f)

        run('docker', 'run', '-v', f'{tmp_path}:/opt/test/', any_image,
            'predict', '/opt/test/input.json', '/opt/test/',
            stream_output=False)

        with open(output_fp) as f:
            result = json.load(f)
            assert result['prediction'] == [[42]]
            assert result['columns'] == ['result']

    finally:
        client = docker.from_env()
        for image in image_remover.images_for_removing:
            client.images.remove(image, force=True)
