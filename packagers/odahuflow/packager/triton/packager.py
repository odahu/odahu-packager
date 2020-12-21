#  Copyright 2020 EPAM Systems
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import enum

import click
import jinja2
import logging
import pathlib
import shutil
import tempfile
import yaml

from odahuflow.packager.helpers.constants import TARGET_DOCKER_REGISTRY
from odahuflow.packager.helpers.docker_builder import build_docker_image, push_docker_image
from odahuflow.packager.helpers.io_proc_utils import setup_logging
from odahuflow.packager.helpers.manifest_and_resource import parse_resource_file, merge_packaging_parameters, \
    save_result, extract_connection_from_resource
from odahuflow.packager.helpers.utils import build_image_name, TemplateNameValues
from .constants import MODEL_MANIFEST_FILE, TRITON_CONFIG_FILE, CONDA_FILE, DOCKERFILE_TEMPLATE_FILE
from .models import PackagingArguments, ModelMeta

log = logging.getLogger(__name__)


class TritonBackends(enum.Enum):
    """This enum contains all supported Triton Backends
    and their corresponding expected names of model file
    """
    Python = 'model.py'
    TensorRT = 'model.plan'
    TensorFlow_SavedModel = 'model.savedmodel'
    TensorFlow_GraphDef = 'model.graphdef'
    ONNX = 'model.onnx'
    TorchScript = 'model.pt'
    Caffe2 = 'model.netdef'


# Set of backends that don't require Triton config file
# https://docs.nvidia.com/deeplearning/triton-inference-server/master-user-guide/docs/model_configuration.html#generated-model-configuration
optional_config_backends = {TritonBackends.TensorRT, TritonBackends.TensorFlow_SavedModel, TritonBackends.ONNX}


resources_dir = pathlib.Path(__file__).parent / 'resources'
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(resources_dir))


@click.command()
@click.argument('model_dir', type=click.Path(exists=True, dir_okay=True, readable=True, resolve_path=True))
@click.argument('packager_file', type=click.Path(exists=True, file_okay=True, readable=True, resolve_path=True))
@click.option('--verbose', is_flag=True, help='Verbose output')
def pack(model_dir, packager_file, verbose):
    setup_logging(verbose)
    model_dir = pathlib.Path(model_dir)
    resource_info = parse_resource_file(packager_file)

    docker_target_connection = extract_connection_from_resource(resource_info, TARGET_DOCKER_REGISTRY)
    arguments = PackagingArguments(**merge_packaging_parameters(resource_info))
    model_repo_dir = pathlib.Path(tempfile.mkdtemp())
    log.info(f'Using {model_repo_dir} as temporary model repository')

    model_dir_files = set((p.name for p in model_dir.iterdir()))
    not_to_copy = set()

    # Reading/generating Model metadata
    if MODEL_MANIFEST_FILE in model_dir_files:
        with open(model_dir / MODEL_MANIFEST_FILE) as f:
            model_manifest = ModelMeta(**yaml.load(f))
    else:
        model_manifest = ModelMeta(name='model', version='1')

    # Creating a file structure expected by Triton
    output_model_dir = model_repo_dir / model_manifest.name
    model_version_dir = output_model_dir / model_manifest.version
    model_version_dir.mkdir(parents=True)

    # Detecting Triton Backend basing on model file name
    detected_backend = None
    for backend in TritonBackends:
        if backend.value in model_dir_files:
            detected_backend = backend
            break

    if detected_backend is None:
        raise ValueError('No Triton backend suits for provided model. Make sure to name model file properly. '
                         'Refer to Nvidia Triton docs to find expected naming conventions: '
                         'https://docs.nvidia.com/deeplearning/triton-inference-server/master-user-guide/docs/'
                         'model_repository.html#framework-model-definition')

    # Validating that Triton config appears if required for found backend
    config_path = model_dir / TRITON_CONFIG_FILE
    if not config_path.exists() and detected_backend not in optional_config_backends:
        raise ValueError(f'{TRITON_CONFIG_FILE} is required for {detected_backend.name} backend')
    else:
        shutil.copy(config_path, output_model_dir)
        not_to_copy.add(TRITON_CONFIG_FILE)

    # Handling conda file
    conda_file_path = model_dir / CONDA_FILE
    if conda_file_path.exists():
        shutil.copy(conda_file_path, model_repo_dir)
        not_to_copy.add(CONDA_FILE)
    else:
        conda_file_path = None

    # Copying all other arbitrary files into output model directory
    for file in model_dir.iterdir():
        if file.name in not_to_copy:
            continue
        if file.is_dir():
            shutil.copytree(file, model_version_dir)
            continue
        shutil.copy(file, model_version_dir)

    dockerfile_template = jinja_env.get_template(DOCKERFILE_TEMPLATE_FILE)
    dockerfile_content = dockerfile_template.render(
        model_repo=str(model_repo_dir),
        conda_file_path=conda_file_path,
        **merge_packaging_parameters(resource_info)
    )

    dockerfile_name = 'Dockefile'
    with open(model_repo_dir / dockerfile_name, 'w') as dockerfile:
        dockerfile.write(dockerfile_content)

    image_name = build_image_name(
        arguments.imageName,
        TemplateNameValues(Name=model_manifest.name, Version=model_manifest.version)
    )

    build_docker_image(str(model_repo_dir), dockerfile_name, image_name)

    save_result(push_docker_image(image_name, docker_target_connection))
