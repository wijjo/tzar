"""Tzar compare command."""

from typing import Text

import jiig


TASK = jiig.Task(
    description='Compare archive to existing files.',
    args={
        'SOURCE_FOLDER': ('-s', '--source-folder',
                          'Source folder',
                          jiig.arg.path_is_folder,
                          jiig.arg.path_to_absolute,
                          jiig.arg.default('.')),
        'ARCHIVE_PATH': ('Path to source archive file or folder',
                         jiig.arg.path_exists),
    },
)


# For type inspection only.
class Data:
    SOURCE_FOLDER: Text
    ARCHIVE_PATH: Text


@TASK.run
def task_run(_runner: jiig.Runner, _data: Data):
    raise NotImplementedError
