"""Tzar compare command."""

import jiig

from tzar.internal.tzar_task_runner import TzarTaskRunner

from . import arguments


@jiig.task('compare',
           arguments.source_folder_option(),
           arguments.archive_path_argument(),
           description='Compare archive to existing files')
def task_compare(_runner: TzarTaskRunner):
    pass
