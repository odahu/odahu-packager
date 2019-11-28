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
import logging
import os.path
import shutil
import uuid

from odahuflow.packager.cli.data_models import DockerTemplateContext, PackagingResourceArguments
from odahuflow.packager.cli.template import render_packager_template
from odahuflow.packager.helpers.constants import DOCKERFILE_TEMPLATE
from odahuflow.packager.helpers.manifest_and_resource import validate_model_manifest, get_model_manifest


def work(model, output_folder, arguments: PackagingResourceArguments):
    """
    Create Model CLI API  (does packaging) from Legion's General Python Prediction Interface (GPPI)

    :param arguments:
    :param model: Path to Legion's General Python Prediction Interface (GPPI) (zip archive unpacked to folder)
    :param output_folder: Path to save results to
    :param conda_env:
    :param ignore_conda:
    :param conda_env_name:
    :param dockerfile:
    :return: model manifest
    """
    # Use absolute paths
    model = os.path.abspath(model)
    output_folder = os.path.abspath(output_folder)

    # Parse and validate manifest
    manifest = get_model_manifest(model)
    validate_model_manifest(manifest)

    logging.info('Model information - name: %s, version: %s', manifest.model.name, manifest.model.version)
    # Copying of model to destination subdirectory
    logging.info(f'Copying {model} to {output_folder}')
    shutil.copytree(model, os.path.join(output_folder, 'gppi'))
    context = DockerTemplateContext(
        model_location='gppi',
        conda_env_name=str(uuid.uuid4()),
        conda_file_name=manifest.binaries.conda_path,
        model_name=manifest.model.name,
        model_version=manifest.model.version,
        base_image=arguments.dockerfileBaseImage
    )

    dockerfile_content = render_packager_template(DOCKERFILE_TEMPLATE, context.dict())
    dockerfile_target = os.path.join(output_folder, DOCKERFILE_TEMPLATE)
    logging.info(f'Dumping {DOCKERFILE_TEMPLATE} to {dockerfile_target}')
    with open(dockerfile_target, 'w') as out_stream:
        out_stream.write(dockerfile_content)

    return manifest


