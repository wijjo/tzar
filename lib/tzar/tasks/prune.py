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
    help='prune archives to save space [destructive]',
    arguments=[
        ('--age-max',
         'AGE_MAX'),
        ('--age-min',
         'AGE_MIN'),
        (['-f', '--archive-folder'],
         'ARCHIVE_FOLDER'),
        ('--date-max',
         'DATE_MAX'),
        ('--date-min',
         'DATE_MIN'),
        ('--interval-max',
         'INTERVAL_MAX'),
        ('--interval-min',
         'INTERVAL_MIN'),
        ('--no-confirmation',
         'NO_CONFIRMATION'),
        ('--size-unit-binary',
         'SIZE_UNIT_BINARY'),
        ('--size-unit-decimal',
         'SIZE_UNIT_DECIMAL'),
        (['-n', '--name'],
         'SOURCE_NAME'),
        (['-s', '--source-folder'],
         'SOURCE_FOLDER'),
        (['-t', '--tags'],
         'TAGS'),
    ],
)
def task_prune(runner: TzarTaskRunner):
    for item in runner.list_catalog():
        print('-->', item.time_string)
