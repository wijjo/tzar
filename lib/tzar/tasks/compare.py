"""Tzar compare command."""

from jiig import task, TaskRunner


@task(
    'compare',
    help='compare archive to existing files',
    options={
    },
    arguments=[
        {
            'dest': 'SOURCE_ARCHIVE',
            'help': 'source archive file or folder',
        },
        {
            'dest': 'ARCHIVE_FOLDER',
            'help': 'archive folder (default: working folder)',
        },
    ],
)
def task_compare(runner: TaskRunner):
    pass
