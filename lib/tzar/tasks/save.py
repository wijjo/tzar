"""Tzar save command."""

import os

from jiig import task

from tzar import TzarTaskRunner


@task(
    'save',
    help='save an archive of the working folder',
    options={
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
        ('-T', '--no-timestamp'): {
            'dest': 'DISABLE_TIMESTAMP',
            'action': 'store_true',
            'help': f'disable adding timestamp to name',
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
    common_options=['ARCHIVE_FOLDER', 'SOURCE_NAME', 'METHOD', 'TAGS'],
    common_arguments=['SOURCE_FOLDER*'],
)
def task_save(runner: TzarTaskRunner):
    for source_folder in runner.args.SOURCE_FOLDER or [os.getcwd()]:
        archiver = runner.create_archiver(source_name=runner.args.SOURCE_NAME,
                                          source_folder=source_folder,
                                          archive_folder=runner.args.ARCHIVE_FOLDER)
        archiver.save_archive(runner.args.METHOD,
                              gitignore=runner.args.GITIGNORE,
                              excludes=runner.args.EXCLUDE,
                              pending=runner.args.PENDING,
                              timestamp=not runner.args.DISABLE_TIMESTAMP,
                              progress=runner.args.PROGRESS,
                              keep_list=runner.args.KEEP_LIST,
                              tags=runner.args.TAGS)
