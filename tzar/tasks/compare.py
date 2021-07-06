"""Tzar compare command."""

import jiig

from tzar import arguments
from tzar.runtime import TzarRuntime


# noinspection PyUnusedLocal
@jiig.task
def compare(
    _runtime: TzarRuntime,
    archive_path: arguments.archive_path_argument,
    source_folder: arguments.source_folder_option,
):
    """Compare archive to existing files."""
    raise NotImplementedError
