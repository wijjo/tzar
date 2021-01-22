"""Tzar compare command."""

from typing import Text

from jiig import arg, model


class TaskClass(model.Task):
    """Compare archive to existing files."""

    # For type inspection only.
    class Data:
        SOURCE_FOLDER: Text
        ARCHIVE_PATH: Text
    data: Data

    args = {
        'SOURCE_FOLDER': ('-s', '--source-folder',
                          'Source folder',
                          arg.path_is_folder,
                          arg.path_to_absolute,
                          arg.default('.')),
        'ARCHIVE_PATH': ('Path to source archive file or folder',
                         arg.path_exists),
    }

    def on_run(self):
        pass
