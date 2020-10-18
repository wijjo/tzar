"""Tzar prune command."""

from jiig import task

from tzar import TzarTaskRunner


@task(
    'delete',
    help='delete archive(s) [destructive]',
    arguments=[
        'ARCHIVE_PATH+',
    ],
)
def task_delete(_runner: TzarTaskRunner):
    pass
