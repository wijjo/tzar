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
            'dest': 'TARGET_FOLDER',
            'help': 'target folder (default: working folder)',
        },
    ],
)
def task_compare(runner: TaskRunner):
    pass
