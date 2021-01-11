# Description

Main aim of this packager is to provide an ability to pack models,
saved in "Odahu's General Python Prediction Interface (GPPI)" format.

As a result of packager you receives bash script to run HTTP REST service using gunicorn
with all required files to do it. Also this script creates conda environment to be used in serving phase.

To make Docker repository, you may:

1. Run this script in Dockerfile
2. Use S2I or other specialized projects.
3. Built Docker image using any tool that provides capability to place some directories to image.

## Installation

Please install `odahuflow-rest-packager` Python package
using your favourite package management tool (pip, pipenv or etc.).


## Usage

To run packager, please [install it](#installation) and call `odahu-flow-pack-to-rest` script from CLI,
or import `odahuflow.packager.flask` module and call `work` function.

This function accepts path to saved model (path to zip archive or already unpacked directory)
and target path (where result REST service should be placed). Also this function contains
other configuration parameters that can be used for configuring your REST HTTP service parameters.

To get other parameters, please run tool with `--help` option.

## Credentials
Odahu Platform Team, 2019
Apache License, Version 2.0, January 2004
