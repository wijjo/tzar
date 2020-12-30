"""Tzar compare command."""

from tzar.internal.tzar_task import TzarTask

from . import arguments


class TaskClass(TzarTask):
    """Compare archive to existing files."""
    opts = [
        arguments.source_folder_option(),
    ]
    args = [
        arguments.archive_path_argument(),
    ]

    def on_run(self):
        pass
