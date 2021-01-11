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

import pydantic

from odahuflow.packager.helpers.constants import DEFAULT_IMAGE_NAME_TEMPLATE


class PackagingResourceArguments(pydantic.BaseModel):
    """
    Odahu Packaging Resource Arguments
    """

    dockerfilePush: bool = True
    dockerfileAddCondaInstallation: bool = True
    dockerfileBaseImage: str = 'odahu/odahu-flow-docker-packager-base:latest'
    dockerfileCondaEnvsLocation: str = '/opt/conda/envs/'
    # Full name or Jinja template
    imageName: str = DEFAULT_IMAGE_NAME_TEMPLATE


class DockerTemplateContext(pydantic.BaseModel):
    """
    Main Docker template context
    """

    base_image: str
    conda_file_name: str
    model_name: str
    model_version: str
    model_location: str
    gppi_location: str
    entrypoint_invoker_script: str  # script that invoke gppi entrypoint
    entrypoint_invoker_cli_name: str  # cli (refers to ::main():: of ::entrypoint_invoker_script::)
    entrypoint: str  # entrypoint that is described in GPPI manifest
    package_name: str  # package name that  will be packed to distro (setuptools)
    distro_name: str  # setuptools distributive name
