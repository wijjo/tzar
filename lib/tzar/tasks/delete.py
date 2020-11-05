"""Tzar prune command."""

from jiig import task
from tzar.internal.task_runner import TzarTaskRunner
from .arguments import archive_path_argument


@task('delete',
      archive_path_argument(positional=True, cardinality='+'),
      description='Delete archive(s) [destructive]')
def task_delete(_runner: TzarTaskRunner):
    pass
