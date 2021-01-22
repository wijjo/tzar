"""
Tzar prune command.

Pruning options provide flexibility for specifying different algorithms for
choosing which archives to purge.

Due to the destructive nature of these actions, an action summary is displayed,
followed by a confirmation prompt. A NO_CONFIRMATION option can disable the
confirmation prompt, e.g. for automation scripts.
"""

import os
from typing import Optional, Text, List

from jiig import model, arg

from tzar.internal.constants import DEFAULT_ARCHIVE_FOLDER
from tzar.internal.archiver import create_archiver


class TaskClass(model.Task):
    """Prune archives to save space [destructive]."""

    # For type inspection only.
    class Data:
        AGE_MAX: Optional[float]
        AGE_MIN: Optional[float]
        ARCHIVE_FOLDER: Text
        DATE_MAX: Optional[float]
        DATE_MIN: Optional[float]
        INTERVAL_MAX: Optional[int]
        INTERVAL_MIN: Optional[int]
        NO_CONFIRMATION: bool
        SOURCE_NAME: Text
        SOURCE_FOLDER: Text
        TAGS: Optional[List[Text]]
    data: Data

    args = {
        'AGE_MAX': ('--age-max',
                    'Maximum archive age [age_option]',
                    arg.str_to_age),
        'AGE_MIN': ('--age-min',
                    'Minimum archive age [age_option]',
                    arg.str_to_age),
        'ARCHIVE_FOLDER': ('-f', '--archive-folder', 'Archive folder',
                           arg.path_is_folder,
                           arg.default(DEFAULT_ARCHIVE_FOLDER)),
        'DATE_MAX': ('--date-max',
                     'Maximum (latest) archive date',
                     arg.str_to_timestamp),
        'DATE_MIN': ('--date-min',
                     'Minimum (earliest) archive date',
                     arg.str_to_timestamp),
        'INTERVAL_MAX': ('--interval-max',
                         'Maximum interval (n[HMS]) between saves to consider',
                         arg.str_to_interval),
        'INTERVAL_MIN': ('--interval-min',
                         'Minimum interval (n[HMS]) between saves to consider',
                         arg.str_to_interval),
        'NO_CONFIRMATION!': ('--no-confirmation',
                             'Execute destructive actions without prompting for confirmation'),
        'SOURCE_NAME': ('-n', '--name',
                        'Source name',
                        arg.default(os.path.basename(os.getcwd()))),
        'SOURCE_FOLDER': ('-s', '--source-folder',
                          'Source folder',
                          arg.path_is_folder,
                          arg.path_to_absolute,
                          arg.default('.')),
        'TAGS': ('-t', '--tags',
                 'Comma-separated archive tags',
                 arg.str_to_comma_tuple),
    }

    def on_run(self):
        archiver = create_archiver(self.data.SOURCE_FOLDER,
                                   self.data.ARCHIVE_FOLDER,
                                   source_name=self.data.SOURCE_NAME,
                                   verbose=self.runtime.verbose,
                                   dry_run=self.runtime.dry_run)
        for item in archiver.list_catalog(
                date_min=self.data.DATE_MIN,
                date_max=self.data.DATE_MAX,
                age_min=self.data.AGE_MIN,
                age_max=self.data.AGE_MAX,
                interval_min=self.data.INTERVAL_MIN,
                interval_max=self.data.INTERVAL_MAX,
                tags=self.data.TAGS):
            print('-->', item.time_string)
