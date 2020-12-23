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
import re

from odahuflow.packager.helpers.constants import DEFAULT_IMAGE_NAME_TEMPLATE


class PackagingArguments(pydantic.BaseModel):
    triton_base_image_tag: str = '20.11-py3'
    # Full name or Jinja template
    imageName: str = DEFAULT_IMAGE_NAME_TEMPLATE


class ModelMeta(pydantic.BaseModel):
    name: str
    version: str

    @pydantic.validator('name')
    def must_be_valid_url_path_segment(cls, v):  # pylint: disable=no-self-argument
        url_path_segment_re = r'^[/.a-zA-Z0-9-_]+$'
        assert re.match(url_path_segment_re, v), 'Model name must be valid URL path segment'
        return v

    @pydantic.validator('version')
    def must_be_numeric(cls, v):  # pylint: disable=no-self-argument
        assert v.isnumeric(), 'Model version must be numeric'
        return v
