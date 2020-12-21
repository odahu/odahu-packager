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
import os.path

import logging
import shutil
import uuid
from odahuflow.sdk.gppi import entrypoint_invoke

from odahuflow.packager.cli.constants import PACKAGE_NAME, ENTRYPOINT_INVOKER_SCRIPT, ENTRYPOINT_INVOKER_CLI_NAME
from odahuflow.packager.cli.data_models import DockerTemplateContext, PackagingResourceArguments
from odahuflow.packager.cli.template import render_packager_template
from odahuflow.packager.helpers.constants import DOCKERFILE_TEMPLATE, ODAHU_SUB_PATH_NAME, GPPI_LOCATION
from odahuflow.packager.helpers.manifest_and_resource import validate_model_manifest, get_model_manifest


def work(model, output_folder, arguments: PackagingResourceArguments):
    """
    Create Model CLI API  (does packaging) from Odahu's General Python Prediction Interface (GPPI)

    :param arguments:
    :param model: Path to Odahu's General Python Prediction Interface (GPPI) (zip archive unpacked to folder)
    :param output_folder: Path to save results to
    :param conda_env:
    :param ignore_conda:
    :param dockerfile:
    :return: model manifest
    """

    # Use absolute paths
    model = os.path.abspath(model)
    output_folder = os.path.abspath(output_folder)

    # Parse and validate manifest
    manifest = get_model_manifest(model)
    validate_model_manifest(manifest)

    context = DockerTemplateContext(
        gppi_location=GPPI_LOCATION,
        model_location=ODAHU_SUB_PATH_NAME,
        conda_file_name=manifest.binaries.conda_path,
        model_name=manifest.model.name,
        model_version=manifest.model.version,
        base_image=arguments.dockerfileBaseImage,
        entrypoint_invoker_script=ENTRYPOINT_INVOKER_SCRIPT,
        entrypoint_invoker_cli_name=ENTRYPOINT_INVOKER_CLI_NAME,
        entrypoint=manifest.model.entrypoint,
        package_name=PACKAGE_NAME,
        distro_name=f'{manifest.model.name}-{str(uuid.uuid4())[:8]}'
    )

    logging.info('Model information - name: %s, version: %s', manifest.model.name, manifest.model.version)
    # Copying of model to destination subdirectory
    logging.info(f'Copying {model} to {output_folder}')
    shutil.copytree(model, os.path.join(output_folder, GPPI_LOCATION))

    # create gppi entrypoint invoker package
    target_entrypoint = os.path.join(output_folder, PACKAGE_NAME, f'{ENTRYPOINT_INVOKER_SCRIPT}.py')
    local_entrypoint = entrypoint_invoke.__file__
    logging.info(f'Copying entrypoit invoker {local_entrypoint} to {target_entrypoint}')
    os.makedirs(os.path.join(output_folder, PACKAGE_NAME), exist_ok=True)
    open(os.path.join(output_folder, PACKAGE_NAME, '__init__.py'), 'a').close()
    shutil.copy(local_entrypoint, target_entrypoint)

    # copy cli setup
    setup_content = render_packager_template('setup.py', context.dict())
    setup_target = os.path.join(output_folder, 'setup.py')
    logging.info(f'Dumping setup.py to {setup_target}')
    with open(setup_target, 'w') as out_stream:
        out_stream.write(setup_content)

    dockerfile_content = render_packager_template(DOCKERFILE_TEMPLATE, context.dict())
    dockerfile_target = os.path.join(output_folder, DOCKERFILE_TEMPLATE)
    logging.info(f'Dumping {DOCKERFILE_TEMPLATE} to {dockerfile_target}')
    with open(dockerfile_target, 'w') as out_stream:
        out_stream.write(dockerfile_content)

    return manifest
