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

from odahuflow.packager.helpers.constants import DESCRIPTION_TEMPLATE
from odahuflow.packager.rest.template import render_packager_template


def test_render_packager_template():
    values = dict(
        model_name="test",
        model_version='7.8.9',
        odahuflow_version='4.5.6',
        packager_version='1.2.3',
    )

    rendered_description = render_packager_template(DESCRIPTION_TEMPLATE, values)
    for _, value in values.items():
        assert value in rendered_description
