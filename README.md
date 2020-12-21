# 1. About

This repository contains MLFlow integration toolchain for [Legion platform](https://github.com/legion-platform/legion).

# 2. What does it do?

Legion's toolchain for MLFlow is responsible for running process of training MLFlow models. It produces model as ZIP archive in Legion's General Python Prediction Interface.

# 3. Requirements

This toolchain requires MLFlow tracking server to be installed (MLFlow tracking server is bundled in HELM Chart).


# Packaging Integration Interface

Packager's container runs as a part of Tekton pipeline. 

Container's command (entrypoint in Docker's terms) is taken from `entrypoint` field of `PackagingIntegration` object.
The command is also provided by 2 arguments:
- path to unzipped model artifact directory
- path to `K8sPackager` manifest file
