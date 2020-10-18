"""Tzar compare command."""

from jiig import task

from tzar import TzarTaskRunner


@task(
    'compare',
    help='compare archive to existing files',
    arguments=[
        'ARCHIVE_PATH',
        'SOURCE_FOLDER',
    ]
)
def task_compare(_runner: TzarTaskRunner):
    pass
