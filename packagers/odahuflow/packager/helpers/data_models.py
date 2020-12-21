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

#
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
Data models (validation by pydantic)
"""
import pydantic
import typing


class OdahuProjectManifestBinaries(pydantic.BaseModel):
    """
    Odahu Project Manifest's Binaries description
    """

    type: str
    dependencies: str
    conda_path: typing.Optional[str]


class OdahuProjectManifestModel(pydantic.BaseModel):
    """
    Odahu Project Manifest's Model description
    """

    name: str
    version: str
    workDir: str
    entrypoint: str


class OdahuProjectManifestToolchain(pydantic.BaseModel):
    """
    Odahu Project Manifest's Toolchain description
    """

    name: str
    version: str


class OdahuProjectManifest(pydantic.BaseModel):
    """
    Odahu Project Manifest description class
    """

    binaries: OdahuProjectManifestBinaries
    model: typing.Optional[OdahuProjectManifestModel]
    odahuflowVersion: typing.Optional[str]
    toolchain: typing.Optional[OdahuProjectManifestToolchain]
