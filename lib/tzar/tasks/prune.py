"""Tzar prune command."""

from jiig import task

from tzar import TzarTaskRunner


@task(
    'prune',
    help='prune archives to save space',
    common_options=['ARCHIVE_FOLDER', 'SOURCE_NAME'],
)
def task_prune(_runner: TzarTaskRunner):
    pass
