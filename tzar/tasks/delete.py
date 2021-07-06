"""Tzar delete command."""

import jiig

from tzar import arguments
from tzar.runtime import TzarRuntime


# noinspection PyUnusedLocal
@jiig.task
def delete(
    runtime: TzarRuntime,
    archive_path: arguments.archive_paths_argument,
):
    """Delete archive(s). [^destructive]"""
    raise NotImplementedError
