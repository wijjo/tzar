"""Tzar compare command."""

from typing import Text

import jiig


class TaskClass(jiig.Task):
    """Compare archive to existing files."""

    # For type inspection only.
    class Data:
        SOURCE_FOLDER: Text
        ARCHIVE_PATH: Text
    data: Data

    args = {
        'SOURCE_FOLDER': ('-s', '--source-folder',
                          'Source folder',
                          jiig.path.check_folder,
                          jiig.path.absolute,
                          jiig.Default('.')),
        'ARCHIVE_PATH': ('Path to source archive file or folder',
                         jiig.path.check_exists),
    }

    def on_run(self):
        pass
