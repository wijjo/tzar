"""Tzar save command."""

import os

from jiig import task, TaskRunner

from tzar.archiver import create_archiver, get_method_names, DEFAULT_METHOD
from tzar.constants import DEFAULT_ARCHIVE_FOLDER


@task(
    'save',
    help='save an archive of the working folder',
    options={
        ('-e', '--exclude'): {
            'dest': 'EXCLUDE',
            'nargs': '*',
            'help': 'exclusion pattern(s), including gitignore-style wildcards',
        },
        ('-f', '--archive-folder'): {
            'dest': 'ARCHIVE_FOLDER',
            'default': DEFAULT_ARCHIVE_FOLDER,
            'help': f'archive folder (default: "{DEFAULT_ARCHIVE_FOLDER}")',
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
        '--keep-list': {
            'dest': 'KEEP_LIST',
            'action': 'store_true',
            'help': 'do not delete temporary file list when done',
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
    archiver = create_archiver(archive_folder=runner.args.ARCHIVE_FOLDER,
                               verbose=runner.verbose,
                               dry_run=runner.dry_run)
    for source_folder in runner.args.SOURCE_FOLDER or [os.getcwd()]:
        archiver.save_archive(source_folder,
                              runner.args.METHOD,
                              gitignore=runner.args.GITIGNORE,
                              excludes=runner.args.EXCLUDE,
                              pending=runner.args.PENDING,
                              timestamp=runner.args.TIMESTAMP,
                              progress=runner.args.PROGRESS,
                              keep_list=runner.args.KEEP_LIST)
