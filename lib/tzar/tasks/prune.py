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

from jiig import BoolOpt, Opt, adapters, Task

from tzar.internal.constants import DEFAULT_ARCHIVE_FOLDER
from tzar.internal.archiver import create_archiver


class TaskClass(Task):
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

    args = [
        Opt('--age-max', 'AGE_MAX', 'Maximum archive age [age_option]',
            adapters.time.age),
        Opt('--age-min', 'AGE_MIN', 'Minimum archive age [age_option]',
            adapters.time.age),
        Opt(('-f', '--archive-folder'), 'ARCHIVE_FOLDER', 'Archive folder',
            adapters.path.check_folder,
            default_value=DEFAULT_ARCHIVE_FOLDER),
        Opt('--date-max', 'DATE_MAX', 'Maximum (latest) archive date',
            adapters.time.timestamp),
        Opt('--date-min', 'DATE_MIN', 'Minimum (earliest) archive date',
            adapters.time.timestamp),
        Opt('--interval-max', 'INTERVAL_MAX',
            'Maximum interval (n[HMS]) between saves to consider',
            adapters.time.interval),
        Opt('--interval-min', 'INTERVAL_MIN',
            'Minimum interval (n[HMS]) between saves to consider',
            adapters.time.interval),
        BoolOpt('--no-confirmation', 'NO_CONFIRMATION',
                'Execute destructive actions without prompting for confirmation'),
        Opt(('-n', '--name'), 'SOURCE_NAME', 'Source name',
            default_value=os.path.basename(os.getcwd())),
        Opt(('-s', '--source-folder'), 'SOURCE_FOLDER', 'Source folder',
            adapters.path.check_folder,
            adapters.path.absolute,
            default_value='.'),
        Opt(('-t', '--tags'), 'TAGS', 'Comma-separated archive tags',
            adapters.text.comma_tuple),
    ]

    def on_run(self):
        archiver = create_archiver(self.data.SOURCE_FOLDER,
                                   self.data.ARCHIVE_FOLDER,
                                   source_name=self.data.SOURCE_NAME,
                                   verbose=self.params.VERBOSE,
                                   dry_run=self.params.DRY_RUN)
        for item in archiver.list_catalog(
                date_min=self.data.DATE_MIN,
                date_max=self.data.DATE_MAX,
                age_min=self.data.AGE_MIN,
                age_max=self.data.AGE_MAX,
                interval_min=self.data.INTERVAL_MIN,
                interval_max=self.data.INTERVAL_MAX,
                tags=self.data.TAGS):
            print('-->', item.time_string)
