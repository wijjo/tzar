"""Tzar save command."""

import os

import time

from jiig import task, TaskRunner
from jiig.utility.filesystem import chdir, create_folder

from tzar import constants
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
            'default': constants.DEFAULT_TARGET,
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
    target_template = time.strftime(runner.args.TARGET)
    archiver = create_archiver(runner.args.METHOD,
                               dry_run=runner.dry_run)
    source_folders = runner.args.SOURCE_FOLDER
    if not source_folders:
        source_folders = [os.getcwd()]
    for source_folder in source_folders:
        with chdir(source_folder):
            relative_target_path = target_template.format(
                name=os.path.basename(os.getcwd()))
            absolute_target_path = os.path.abspath(relative_target_path)
            create_folder(os.path.dirname(absolute_target_path))
            archiver.save(source_folder,
                          absolute_target_path,
                          verbose=runner.verbose,
                          progress=runner.args.PROGRESS,
                          keep_list=runner.args.KEEP_LIST)
