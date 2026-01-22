import copy
from typing import List, Optional

import click
import rich
from openff.toolkit import ForceField
from openff.toolkit.utils.exceptions import ParameterLookupError
from rich import pretty
from rich.padding import Padding

from openff.bespokefit.cli.utilities import exit_with_messages, print_header


@click.command("combine")
@click.option(
    "--output",
    "output_file",
    type=click.STRING,
    help="The name of the file the combined force field should be wrote to.",
    required=True,
)
@click.option(
    "--ff",
    "force_field_files",
    type=click.Path(exists=True, dir_okay=False),
    help="The file name of any local force fields to include in the combined force field.",
    required=False,
    multiple=True,
)
def combine_cli(
    output_file: str,
    force_field_files: Optional[List[str]],
):
    """
    Combine force fields from local files.
    """
    pretty.install()

    console = rich.get_console()
    print_header(console)

    if not force_field_files:
        exit_with_messages(
            "[[red]ERROR[/red]] At least one `--ff` must be specified",
            console=console,
            exit_code=2,
        )

    all_force_fields = [
        ForceField(force_field, load_plugins=True, allow_cosmetic_attributes=True)
        for force_field in force_field_files
    ]

    # Now combine all unique torsions
    master_ff = copy.deepcopy(all_force_fields[0])
    for ff in all_force_fields[1:]:
        for parameter in ff.get_parameter_handler("ProperTorsions").parameters:
            try:
                _ = master_ff.get_parameter_handler("ProperTorsions")[parameter.smirks]
            except ParameterLookupError:
                master_ff.get_parameter_handler("ProperTorsions").add_parameter(
                    parameter=parameter
                )

    master_ff.to_file(filename=output_file, discard_cosmetic_attributes=True)

    message = Padding(
        f"The combined force field has been saved to [repr.filename]{output_file}[/repr.filename]",
        (1, 0, 1, 0),
    )
    console.print(message)
