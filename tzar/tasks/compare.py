"""Tzar compare command."""

import jiig

from tzar import arguments
from tzar.runtime import TzarRuntime


class Task(jiig.Task):
    """Compare archive to existing files."""

    archive_path: arguments.archive_path_argument
    source_folder: arguments.source_folder_option

    def on_run(self, _runtime: TzarRuntime):
        raise NotImplementedError
