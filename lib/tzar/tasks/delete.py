"""Tzar prune command."""

import jiig

from tzar.internal.tzar_task_runner import TzarTaskRunner

from . import arguments


@jiig.task('delete',
           arguments.archive_path_argument(cardinality='+'),
           description='Delete archive(s) [destructive]')
def task_delete(_runner: TzarTaskRunner):
    pass
