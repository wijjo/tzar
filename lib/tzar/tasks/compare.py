"""Tzar compare command."""

from typing import Text

from jiig import Task, Opt, Arg, adapters


class TaskClass(Task):
    """Compare archive to existing files."""

    # For type inspection only.
    class Data:
        SOURCE_FOLDER: Text
        ARCHIVE_PATH: Text
    data: Data

    args = [
        Opt(('-s', '--source-folder'), 'SOURCE_FOLDER', 'Source folder',
            adapters.path.check_folder,
            adapters.path.absolute,
            default_value='.'),
        Arg('ARCHIVE_PATH', 'Path to source archive file or folder',
            adapters.path.check_exists),
    ]

    def on_run(self):
        pass
