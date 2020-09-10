"""Tzar save command."""

import os

from jiig import task, TaskRunner

from tzar.archiver import create_archiver, get_method_names, DEFAULT_METHOD


@task(
    'save',
    help='save an archive of the working folder',
    options={
        ('-e', '--exclude'): {
            'dest': 'EXCLUDE',
            'nargs': '*',
            'help': 'exclusion pattern(s), including unix-style wildcards',
        },
        '--keep-list': {
            'dest': 'KEEP_LIST',
            'action': 'store_true',
            'help': 'do not delete the temporary file list when done',
        },
        ('-m', '--method'): {
            'dest': 'METHOD',
            'choices': get_method_names(),
            'default': DEFAULT_METHOD,
            'help': f'archive method (default: "{DEFAULT_METHOD}")',
        },
        ('-p', '--progress'): {
            'dest': 'PROGRESS',
            'action': 'store_true',
            'help': 'display progress statistics'
        },
        ('-t', '--target'): {
            'dest': 'TARGET',
            'help': 'target folder and name specification',
        },
        '--gitignore': {
            'dest': 'GITIGNORE',
            'action': 'store_true',
            'help': 'use .gitignore exclusions',
        },
        '--pending': {
            'dest': 'PENDING',
            'action': 'store_true',
            'help': 'save only modified version-controlled files',
        },
    },
    arguments=[
        {
            'dest': 'SOURCE_FOLDER',
            'nargs': '*',
            'help': 'source folder(s) (default: working folder)',
        },
    ],
)
def task_save(runner: TaskRunner):
    archiver = create_archiver(runner.args.METHOD,
                               target_spec=runner.args.TARGET,
                               verbose=runner.verbose,
                               dry_run=runner.dry_run)
    for source_folder in runner.args.SOURCE_FOLDER or [os.getcwd()]:
        archiver.save(source_folder,
                      progress=runner.args.PROGRESS,
                      keep_list=runner.args.KEEP_LIST)
