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

from odahuflow.packager.helpers.constants import ODAHU_SUB_PATH_NAME, HANDLER_MODULE, \
    CONDA_FILE_NAME, ENTRYPOINT_TEMPLATE, HANDLER_APP, DOCKERFILE_TEMPLATE, CONDA_SERVER_FILE_NAME
from odahuflow.packager.helpers.data_models import OdahuProjectManifest
from odahuflow.packager.helpers.io_proc_utils import make_executable
from odahuflow.packager.helpers.manifest_and_resource import validate_model_manifest, get_model_manifest
from odahuflow.packager.flask.constants import RESOURCES_FOLDER
from odahuflow.packager.flask.data_models import PackagingResourceArguments, DockerTemplateContext
from odahuflow.packager.flask.template import render_packager_template


def work(model, output_folder, arguments: PackagingResourceArguments):
    """
    Create REST API wrapper (does packaging) from Odahu's General Python Prediction Interface (GPPI)

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

    # Output status to console
    logging.info(f'Trying to make REST service from model {model} in {output_folder}')

    # Parse and validate manifest
    manifest = get_model_manifest(model)
    validate_model_manifest(manifest)

    logging.info('Model information - name: %s, version: %s', manifest.model.name, manifest.model.version)
    conda_dep_list = os.path.join(model, manifest.binaries.conda_path)
    # Choose name for conda env name
    context = _generate_template_context(arguments, manifest, output_folder)

    # Building of variables for template file and generating of output
    final_entrypoint = render_packager_template(ENTRYPOINT_TEMPLATE, context.dict())

    # Copying of model to destination subdirectory
    model_location = os.path.join(model, manifest.model.workDir)
    target_model_location = os.path.join(output_folder, ODAHU_SUB_PATH_NAME)

    logging.info(f'Copying {model_location} to {target_model_location}')
    shutil.copytree(model_location, target_model_location)

    # Copying of handler function
    handler_location = os.path.join(RESOURCES_FOLDER, f'{HANDLER_MODULE}.py')
    target_handler_location = os.path.join(output_folder, f'{HANDLER_MODULE}.py')

    logging.info(f'Copying handler {handler_location} to {target_handler_location}')
    shutil.copy(handler_location, target_handler_location)

    # Copying of conda env
    target_conda_env_location = os.path.join(output_folder, CONDA_FILE_NAME)
    logging.info(f'Copying handler {conda_dep_list} to {target_conda_env_location}')
    shutil.copy(conda_dep_list, target_conda_env_location)

    # Copying of server conda file
    server_conda_env_location = os.path.join(RESOURCES_FOLDER, CONDA_SERVER_FILE_NAME)
    target_server_conda_env_location = os.path.join(output_folder, CONDA_SERVER_FILE_NAME)
    logging.info(f'Copying server conda file {server_conda_env_location} to {target_server_conda_env_location}')
    shutil.copy(server_conda_env_location, target_server_conda_env_location)

    entrypoint_target = os.path.join(output_folder, ENTRYPOINT_TEMPLATE)
    logging.info(f'Dumping {ENTRYPOINT_TEMPLATE} to {entrypoint_target}')
    with open(entrypoint_target, 'w', encoding='utf-8') as out_stream:
        out_stream.write(final_entrypoint)

    dockerfile_content = render_packager_template(DOCKERFILE_TEMPLATE, context.dict())
    dockerfile_target = os.path.join(output_folder, DOCKERFILE_TEMPLATE)
    logging.info(f'Dumping {DOCKERFILE_TEMPLATE} to {dockerfile_target}')

    with open(dockerfile_target, 'w', encoding='utf-8') as out_stream:
        out_stream.write(dockerfile_content)
    make_executable(dockerfile_target)

    return manifest


def _generate_template_context(arguments: PackagingResourceArguments,
                               manifest: OdahuProjectManifest,
                               output_folder: str) -> DockerTemplateContext:
    """
    Generate Docker packager context for templates
    """
    logging.info('Building context for template')

    return DockerTemplateContext(
        model_name=manifest.model.name,
        model_version=manifest.model.version,
        odahuflow_version=manifest.odahuflowVersion,
        timeout=arguments.timeout,
        host=arguments.host,
        port=arguments.port,
        workers=arguments.workers,
        threads=arguments.threads,
        pythonpath=output_folder,
        wsgi_handler=f'{HANDLER_MODULE}:{HANDLER_APP}',
        model_location=ODAHU_SUB_PATH_NAME,
        entrypoint_target=ENTRYPOINT_TEMPLATE,
        handler_file=f'{HANDLER_MODULE}.py',
        base_image=arguments.dockerfileBaseImage,
        conda_file_name=CONDA_FILE_NAME,
        conda_server_file_name=CONDA_SERVER_FILE_NAME,
        entrypoint_docker=ENTRYPOINT_TEMPLATE
    )
