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
import os
import re

from setuptools import find_namespace_packages, setup

PACKAGE_ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
VERSION_FILE = os.path.join(PACKAGE_ROOT_PATH, 'odahuflow/packager/rest', 'version.py')


def extract_version() -> str:
    """
    Extract version from .py file using regex

    :return: odahuflow version
    """
    with open(VERSION_FILE, 'rt') as version_file:
        file_content = version_file.read()
        VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
        mo = re.search(VSRE, file_content, re.M)
        if mo:
            return mo.group(1)
        else:
            raise RuntimeError("Unable to find version string in %s." % (file_content,))

setup(
    name='odahuflow-rest-packager',
    version=extract_version(),
    description='Legion\'s GPPI to rest CLI',
    packages=find_namespace_packages(),
    url='https://github.com/odahu/odahu-packager',
    author='Vlad Tokarev, Vitalik Solodilov',
    author_email='vlad.tokarev.94@gmail.com, mcdkr@yandex.ru',
    license='Apache v2',
    entry_points={
        'console_scripts': [
            'odahuflow-pack-to-rest=odahuflow.packager.rest:work_resource_file'
        ],
    },
    install_requires=[
        # TODO: change to PyPi when we publish release
        'odahuflow-sdk @ git+https://github.com/odahu/odahu-flow@feat/1079-migration#egg=odahuflow-sdk&subdirectory=odahuFlow/sdk',
        'click>=7.0',
        'urllib3>=1.24.3',
        'pyyaml>=3.1.2',
        'pydantic==0.32.2',
        'docker',
        'botocore>=1.12.75',
        'boto3>=1.9.75',
        'jinja2>=2.7.3'
    ],
    extras_require={
        'testing': [
            'pytest>=5.1.2',
            'pytest-mock>=1.10.4',
            'pytest-cov>=2.7.1',
            'pylint>=2.3.0'
        ]
    },
)
