from setuptools import setup

setup(
    name='{{ model_name }}',
    version='{{ model_version }}',
    description='Odahuflow cli packed {{ model_name }} model', packages=['odahuflow'],
    entry_points={
        'console_scripts': [
            '{{ entrypoint_invoker_cli_name }}=odahuflow.{{ entrypoint_invoker_script }}:main'
        ],
    },
)
