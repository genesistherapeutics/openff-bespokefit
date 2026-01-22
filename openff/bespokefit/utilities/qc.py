"""QC-related utility functions for torsion drive calculations."""

from typing import Any, Dict, List

import psutil
import qcelemental
from openff.toolkit.topology import Atom
from qcengine.config import get_global


def _task_config() -> Dict[str, Any]:
    """
    Returns a task configuration dictionary for QCEngine calculations.

    Returns a dict with ncores, nnodes, memory (in GiB), and retries.
    Uses system defaults from qcengine and psutil.
    """
    n_cores = get_global("ncores")
    max_memory = psutil.virtual_memory().total / (1024**3)  # Convert to GiB

    return dict(ncores=n_cores, nnodes=1, memory=round(max_memory, 3), retries=3)


def _select_atom(atoms: List[Atom]) -> int:
    """
    For a list of atoms, choose the heaviest atom.

    Args:
        atoms: List of Atom objects to choose from.

    Returns:
        The molecule atom index of the heaviest atom.
    """
    candidate = atoms[0]
    for atom in atoms:
        if atom.atomic_number > candidate.atomic_number:
            candidate = atom
    return candidate.molecule_atom_index


def _get_program_keywords(program: str) -> Dict[str, str]:
    """
    Generate a set of pre-defined keywords for the calculation based on the program.
    These are based on experience.

    Args:
        program: The name of the program which will run the calculation.

    Returns:
        A dictionary of program specific keywords.
    """
    keywords = {}
    if program.lower() == "xtb":
        # <https://github.com/openforcefield/openff-bespokefit/issues/238>
        keywords["verbosity"] = "muted"
    return keywords
