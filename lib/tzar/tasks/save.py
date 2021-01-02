"""Tzar save command."""

import os
from typing import Text, Optional, List

import jiig

from tzar.internal.archiver import create_archiver, get_method_names
from tzar.internal.constants import DEFAULT_ARCHIVE_FOLDER
from tzar.methods import DEFAULT_METHOD


class TaskClass(jiig.Task):
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

    args = {
        'EXCLUDE[*]': ('-e', '--exclude',
                       'Exclusion pattern(s), including gitignore-style wildcards'),
        'PROGRESS!': ('-p', '--progress',
                      'Display progress statistics'),
        'DISABLE_TIMESTAMP!': ('-T', '--no-timestamp',
                               'Disable adding timestamp to name'),
        'GITIGNORE!': ('--gitignore',
                       'Use .gitignore exclusions'),
        'KEEP_LIST!': ('--keep-list',
                       'Do not delete temporary file list when done'),
        'PENDING!': ('--pending',
                     'Save only modified version-controlled files'),
        'ARCHIVE_FOLDER': ('-f', '--archive-folder', 'Archive folder',
                           jiig.path.check_folder,
                           jiig.Default(DEFAULT_ARCHIVE_FOLDER)),
        'SOURCE_NAME': ('-n', '--name',
                        'Source name',
                        jiig.Default(os.path.basename(os.getcwd()))),
        'METHOD': ('-m', '--method',
                   'Archive method',
                   jiig.Default(DEFAULT_METHOD),
                   jiig.Choices(*get_method_names())),
        'TAGS': ('-t', '--tags',
                 'Comma-separated archive tags',
                 jiig.text.comma_tuple),
        'SOURCE_FOLDER': ('-s', '--source-folder',
                          'Source folder',
                          jiig.path.check_folder,
                          jiig.path.absolute,
                          jiig.Default('.')),
    }

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
