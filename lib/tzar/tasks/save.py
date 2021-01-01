"""Tzar save command."""

import os
from typing import Text, Optional, List

from jiig import BoolOpt, Opt, adapters, Task

from tzar.internal.archiver import create_archiver, get_method_names
from tzar.internal.constants import DEFAULT_ARCHIVE_FOLDER
from tzar.methods import DEFAULT_METHOD


class TaskClass(Task):
    """Save an archive of the working folder or another folder."""

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
    data: Data

    args = [
        Opt(('-e', '--exclude'), 'EXCLUDE',
            'Exclusion pattern(s), including gitignore-style wildcards',
            cardinality='*'),
        BoolOpt(('-p', '--progress'), 'PROGRESS',
                'Display progress statistics'),
        BoolOpt(('-T', '--no-timestamp'), 'DISABLE_TIMESTAMP',
                'Disable adding timestamp to name'),
        BoolOpt('--gitignore', 'GITIGNORE',
                'Use .gitignore exclusions'),
        BoolOpt('--keep-list', 'KEEP_LIST',
                'Do not delete temporary file list when done'),
        BoolOpt('--pending', 'PENDING',
                'Save only modified version-controlled files'),
        Opt(('-f', '--archive-folder'), 'ARCHIVE_FOLDER', 'Archive folder',
            adapters.path.check_folder,
            default_value=DEFAULT_ARCHIVE_FOLDER),
        Opt(('-n', '--name'), 'SOURCE_NAME', 'Source name',
            default_value=os.path.basename(os.getcwd())),
        Opt(('-m', '--method'), 'METHOD', 'Archive method',
            default_value=DEFAULT_METHOD,
            choices=get_method_names()),
        Opt(('-t', '--tags'), 'TAGS', 'Comma-separated archive tags',
            adapters.text.comma_tuple),
        Opt(('-s', '--source-folder'), 'SOURCE_FOLDER', 'Source folder',
            adapters.path.check_folder,
            adapters.path.absolute,
            default_value='.'),
    ]

    def on_run(self):
        archiver = create_archiver(self.data.SOURCE_FOLDER,
                                   self.data.ARCHIVE_FOLDER,
                                   source_name=self.data.SOURCE_NAME,
                                   verbose=self.params.VERBOSE,
                                   dry_run=self.params.DRY_RUN)
        archiver.save_archive(self.data.METHOD,
                              gitignore=self.data.GITIGNORE,
                              excludes=self.data.EXCLUDE,
                              pending=self.data.PENDING,
                              timestamp=not self.data.DISABLE_TIMESTAMP,
                              progress=self.data.PROGRESS,
                              keep_list=self.data.KEEP_LIST,
                              tags=self.data.TAGS)
