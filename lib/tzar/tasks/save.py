"""Tzar save command."""

import os

from jiig import task

from tzar import TzarTaskRunner


@task(
    'save',
    help='save an archive of the working folder',
    options={
        ('-l', '--label'): {
            'dest': 'LABELS',
            'help': 'comma-separated labels for tagging the archive',
        },
        ('-e', '--exclude'): {
            'dest': 'EXCLUDE',
            'nargs': '*',
            'help': 'exclusion pattern(s), including gitignore-style wildcards',
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
    common_options=['ARCHIVE_FOLDER', 'SOURCE_NAME', 'METHOD'],
    common_arguments=['SOURCE_FOLDER*'],
)
def task_save(runner: TzarTaskRunner):
    archiver = runner.create_archiver(source_name=runner.args.SOURCE_NAME,
                                      archive_folder=runner.args.ARCHIVE_FOLDER,
                                      labels=runner.args.LABELS)
    for source_folder in runner.args.SOURCE_FOLDER or [os.getcwd()]:
        archiver.save_archive(source_folder,
                              runner.args.METHOD,
                              gitignore=runner.args.GITIGNORE,
                              excludes=runner.args.EXCLUDE,
                              pending=runner.args.PENDING,
                              timestamp=runner.args.TIMESTAMP,
                              progress=runner.args.PROGRESS,
                              keep_list=runner.args.KEEP_LIST)
