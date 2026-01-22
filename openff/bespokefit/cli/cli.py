import click

from openff.bespokefit.cli.combine import combine_cli
from openff.bespokefit.cli.prepare import prepare_cli


@click.group()
def cli():
    """The root group for all CLI commands."""


cli.add_command(prepare_cli)
cli.add_command(combine_cli)
