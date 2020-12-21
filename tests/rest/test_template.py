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

from odahuflow.packager.flask.template import render_packager_template
from odahuflow.packager.helpers.constants import ENTRYPOINT_TEMPLATE


def test_render_packager_template():
    values = dict(
        model_location="model_location_value",
        timeout='timeout_value',
        host='host_value',
        port='port_num',
        workers='workers_num',
        threads='threads_value',
        wsgi_handler='wsgi_handler_value'
    )

    rendered_description = render_packager_template(ENTRYPOINT_TEMPLATE, values)
    for _, value in values.items():
        assert value in rendered_description
