# Installing conda

ARG MINICONDA_URL=https://repo.anaconda.com/miniconda/Miniconda3-4.7.12-Linux-x86_64.sh

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 \
    PATH="/opt/conda/bin:${PATH}"

# Install native dependencies
RUN apt-get update --fix-missing && \
    apt-get install -y wget bzip2 ca-certificates git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install conda
RUN wget --quiet ${MINICONDA_URL} -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    conda clean -tipsy && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc

# / Installing conda
