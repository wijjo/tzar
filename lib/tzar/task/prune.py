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

import jiig

from tzar.internal.constants import DEFAULT_ARCHIVE_FOLDER
from tzar.internal.archiver import create_archiver


TASK = jiig.Task(
    description='Prune archives to save space [destructive].',
    args={
        'AGE_MAX': ('--age-max',
                    'Maximum archive age [age_option]',
                    jiig.arg.str_to_age),
        'AGE_MIN': ('--age-min',
                    'Minimum archive age [age_option]',
                    jiig.arg.str_to_age),
        'ARCHIVE_FOLDER': ('-f', '--archive-folder', 'Archive folder',
                           jiig.arg.path_is_folder,
                           jiig.arg.default(DEFAULT_ARCHIVE_FOLDER)),
        'DATE_MAX': ('--date-max',
                     'Maximum (latest) archive date',
                     jiig.arg.str_to_timestamp),
        'DATE_MIN': ('--date-min',
                     'Minimum (earliest) archive date',
                     jiig.arg.str_to_timestamp),
        'INTERVAL_MAX': ('--interval-max',
                         'Maximum interval (n[HMS]) between saves to consider',
                         jiig.arg.str_to_interval),
        'INTERVAL_MIN': ('--interval-min',
                         'Minimum interval (n[HMS]) between saves to consider',
                         jiig.arg.str_to_interval),
        'NO_CONFIRMATION[!]': ('--no-confirmation',
                               'Execute destructive actions without prompting for confirmation'),
        'SOURCE_NAME': ('-n', '--name',
                        'Source name',
                        jiig.arg.default(os.path.basename(os.getcwd()))),
        'SOURCE_FOLDER': ('-s', '--source-folder',
                          'Source folder',
                          jiig.arg.path_is_folder,
                          jiig.arg.path_to_absolute,
                          jiig.arg.default('.')),
        'TAGS': ('-t', '--tags',
                 'Comma-separated archive tags',
                 jiig.arg.str_to_comma_tuple),
    },
)


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


@TASK.run
def task_run(runner: jiig.Runner, data: Data):
    archiver = create_archiver(data.SOURCE_FOLDER,
                               data.ARCHIVE_FOLDER,
                               source_name=data.SOURCE_NAME,
                               verbose=runner.verbose,
                               dry_run=runner.dry_run)
    for item in archiver.list_catalog(
            date_min=data.DATE_MIN,
            date_max=data.DATE_MAX,
            age_min=data.AGE_MIN,
            age_max=data.AGE_MAX,
            interval_min=data.INTERVAL_MIN,
            interval_max=data.INTERVAL_MAX,
            tags=data.TAGS):
        print('-->', item.time_string)
