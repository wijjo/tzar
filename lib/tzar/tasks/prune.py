"""
Tzar prune command.

Pruning options provide flexibility for specifying different algorithms for
choosing which archives to purge.

Due to the destructive nature of these actions, an action summary is displayed,
followed by a confirmation prompt. A NO_CONFIRMATION option can disable the
confirmation prompt, e.g. for automation scripts.
"""
from jiig import task
from tzar import TzarTaskRunner


@task(
    'prune',
    help='prune archives to save space',
    epilog='All destructive operations require confirmation by default.',
    common_options=['AGE_MAX',
                    'AGE_MIN',
                    'ARCHIVE_FOLDER',
                    'DATE_MAX',
                    'DATE_MIN',
                    'INTERVAL_MAX',
                    'INTERVAL_MIN',
                    'NO_CONFIRMATION',
                    'SIZE_UNIT_BINARY',
                    'SIZE_UNIT_DECIMAL',
                    'SOURCE_NAME',
                    'SOURCE_FOLDER',
                    'TAGS'],
)
def task_prune(runner: TzarTaskRunner):
    for item in runner.list_catalog():
        print('-->', item.time_string)
