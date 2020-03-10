#
#    Copyright 2020 EPAM Systems
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

FROM fedora:31

ARG PIP_EXTRA_INDEX_URL
ENV WORK_DIR="/opt/odahu-flow"
WORKDIR "${WORK_DIR}/"

RUN dnf -y update && dnf -y reinstall shadow-utils && \
    dnf -y install buildah runc python3-pip --exclude container-selinux && \
    rm -rf /var/cache /var/log/dnf* /var/log/yum.*

COPY containers/docker-packager/registries.conf \
     containers/docker-packager/storage.conf \
     /etc/containers/

COPY packagers/docker/requirements.txt "${WORK_DIR}/packagers/docker/requirements.txt"
RUN pip3 install -r "${WORK_DIR}/packagers/docker/requirements.txt"

COPY packagers/docker "${WORK_DIR}/packagers/docker"
RUN pip3 install -e packagers/docker
