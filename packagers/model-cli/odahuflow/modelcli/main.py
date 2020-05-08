import click
from odahuflow.gppi.model.model import Model
from odahuflow.gppi.python.discovery import PythonModelDiscovery


@click.command()
def main():
    models = PythonModelDiscovery().models
    if len(models) != 1:
        raise ValueError("Expected only one model")

    model: Model = models[0]

    print(model.predict([[1, 2, 3]]))