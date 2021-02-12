"""Tzar save command."""

import os
from typing import Text, Optional, List

import jiig

from tzar.internal.archiver import create_archiver, get_method_names
from tzar.internal.constants import DEFAULT_ARCHIVE_FOLDER
from tzar.method import DEFAULT_METHOD


TASK = jiig.Task(
    description='Save an archive of the working folder or another folder.',
    args={
        'EXCLUDE[*]': ('-e', '--exclude',
                       'Exclusion pattern(s), including gitignore-style wildcards'),
        'PROGRESS[!]': ('-p', '--progress',
                        'Display progress statistics'),
        'DISABLE_TIMESTAMP[!]': ('-T', '--no-timestamp',
                                 'Disable adding timestamp to name'),
        'GITIGNORE[!]': ('--gitignore',
                         'Use .gitignore exclusions'),
        'KEEP_LIST[!]': ('--keep-list',
                         'Do not delete temporary file list when done'),
        'PENDING[!]': ('--pending',
                       'Save only modified version-controlled files'),
        'ARCHIVE_FOLDER': ('-f', '--archive-folder', 'Archive folder',
                           jiig.arg.path_is_folder,
                           jiig.arg.default(DEFAULT_ARCHIVE_FOLDER)),
        'SOURCE_NAME': ('-n', '--name',
                        'Source name',
                        jiig.arg.default(os.path.basename(os.getcwd()))),
        'METHOD': ('-m', '--method',
                   'Archive method',
                   jiig.arg.default(DEFAULT_METHOD),
                   jiig.arg.choices(*get_method_names())),
        'TAGS': ('-t', '--tags',
                 'Comma-separated archive tags',
                 jiig.arg.str_to_comma_tuple),
        'SOURCE_FOLDER': ('-s', '--source-folder',
                          'Source folder',
                          jiig.arg.path_is_folder,
                          jiig.arg.path_to_absolute,
                          jiig.arg.default('.')),
    },
)


# Not needed, but serves as a type inspection aid.
class Data:
    EXCLUDE: Optional[List[Text]]
    PROGRESS: bool
    DISABLE_TIMESTAMP: bool
    GITIGNORE: bool
    KEEP_LIST: bool
    PENDING: bool
    ARCHIVE_FOLDER: Optional[Text]
    SOURCE_NAME: Text
    METHOD: Text
    TAGS: Optional[List[Text]]
    SOURCE_FOLDER: Text


@TASK.run
def task_run(runner: jiig.Runner, data: Data):
    archiver = create_archiver(data.SOURCE_FOLDER,
                               data.ARCHIVE_FOLDER,
                               source_name=data.SOURCE_NAME,
                               verbose=runner.verbose,
                               dry_run=runner.dry_run)
    archiver.save_archive(data.METHOD,
                          gitignore=data.GITIGNORE,
                          excludes=data.EXCLUDE,
                          pending=data.PENDING,
                          timestamp=not data.DISABLE_TIMESTAMP,
                          progress=data.PROGRESS,
                          keep_list=data.KEEP_LIST,
                          tags=data.TAGS)
