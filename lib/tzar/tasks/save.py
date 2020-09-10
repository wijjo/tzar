"""Tzar save command."""

import os

from jiig import task, TaskRunner

from tzar.archiver import create_archiver, get_method_names, DEFAULT_METHOD
from tzar.constants import DEFAULT_TARGET_FOLDER


@task(
    'save',
    help='save an archive of the working folder',
    options={
        ('-e', '--exclude'): {
            'dest': 'EXCLUDE',
            'nargs': '*',
            'help': 'exclusion pattern(s), including unix-style wildcards',
        },
        ('-f', '--folder'): {
            'dest': 'FOLDER',
            'default': DEFAULT_TARGET_FOLDER,
            'help': f'target folder (default: "{DEFAULT_TARGET_FOLDER}")',
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
        ('-t', '--timestamp'): {
            'dest': 'TIMESTAMP',
            'action': 'store_true',
            'help': f'append timestamp to name',
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
                               target_folder=runner.args.FOLDER,
                               verbose=runner.verbose,
                               dry_run=runner.dry_run)
    for source_folder in runner.args.SOURCE_FOLDER or [os.getcwd()]:
        archiver.save(source_folder,
                      gitignore=runner.args.GITIGNORE,
                      excludes=runner.args.EXCLUDE,
                      pending=runner.args.PENDING,
                      timestamp=runner.args.TIMESTAMP,
                      progress=runner.args.PROGRESS,
                      keep_list=runner.args.KEEP_LIST)
