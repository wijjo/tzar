"""Tzar save command."""

import os
from typing import Text, Iterator, List

import time

from jiig import task, TaskRunner
from jiig.utility.filesystem import chdir, create_folder, iterate_filtered_files
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
        ('-m', '--method'): {
            'dest': 'METHOD',
            'choices': get_method_names(),
            'default': DEFAULT_METHOD,
            'help': f'archive method (default: "{DEFAULT_METHOD}")',
        },
        ('-p', '--progress'): {
            'dest': 'PROGRESS',
            'action': 'store_true',
            'help': 'display progress bar'
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
            'help': 'save pending locally-changed files',
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
    file_iterator_factory = FileIteratorFactory(pending=runner.args.PENDING,
                                                gitignore=runner.args.GITIGNORE,
                                                excludes=runner.args.EXCLUDE)
    target_template = time.strftime(runner.args.TARGET)
    archiver = create_archiver(runner.args.METHOD, dry_run=runner.dry_run)
    for source_folder in _iterate_folders(runner.args.SOURCE_FOLDER):
        with chdir(source_folder):
            relative_target_path = target_template.format(
                name=os.path.basename(os.getcwd()))
            absolute_target_path = os.path.abspath(relative_target_path)
            create_folder(os.path.dirname(absolute_target_path))
            archiver.save(file_iterator_factory.create_iterator(source_folder),
                          absolute_target_path,
                          verbose=runner.verbose,
                          progress=runner.args.PROGRESS)


def _iterate_folders(source_folders: List[Text]) -> Iterator[Text]:
    if not source_folders:
        yield os.getcwd()
    return source_folders


class FileIteratorFactory:

    def __init__(self,
                 pending: bool = False,
                 gitignore: bool = False,
                 excludes: List[Text] = None):
        self.pending = pending
        self.gitignore = gitignore
        self.excludes = excludes

    def create_iterator(self, folder_path: Text) -> Iterator[Text]:
        return iterate_filtered_files(folder_path,
                                      pending=self.pending,
                                      gitignore=self.gitignore,
                                      excludes=self.excludes)
