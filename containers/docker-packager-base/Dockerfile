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

FROM python:3.6

ARG MINICONDA_URL=https://repo.anaconda.com/miniconda/Miniconda3-4.7.12-Linux-x86_64.sh
ARG CONDA_ENV_PY_VERSION=3.9

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 \
    PATH="/usr/local/nvidia/bin:/opt/conda/bin:${PATH}" \
    LD_LIBRARY_PATH="/usr/local/nvidia/lib64:${LD_LIBRARY_PATH}"

# Install native dependencies
RUN apt-get update --fix-missing && \
    apt-get install -y wget bzip2 ca-certificates git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV ODAHU_CONDA_ENV_NAME=odahu_model
ENV PATH=/opt/conda/envs/${ODAHU_CONDA_ENV_NAME}/bin:$PATH

# Install conda
RUN wget --quiet ${MINICONDA_URL} -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    conda clean -tipsy && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    conda create --name ${ODAHU_CONDA_ENV_NAME} python=${CONDA_ENV_PY_VERSION} --no-default-packages && \
    echo "conda activate ${ODAHU_CONDA_ENV_NAME}" >> ~/.bashrc

WORKDIR /app
