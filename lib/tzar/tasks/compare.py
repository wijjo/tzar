"""Tzar compare command."""

from jiig import task

from tzar.internal.task_runner import TzarTaskRunner

from .arguments import source_folder_argument, archive_path_argument


@task('compare',
      source_folder_argument(),
      archive_path_argument(positional=True),
      description='Compare archive to existing files')
def task_compare(_runner: TzarTaskRunner):
    pass
