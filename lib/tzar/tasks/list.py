"""Tzar list command."""

from time import localtime, strftime
from typing import Text, Tuple

from jiig import task
from jiig.utility.general import format_table

from tzar import TzarTaskRunner, MethodListItem
from tzar.archiver import list_archive


@task(
    'list',
    help='list archive contents',
    arguments=[
        ('--size-unit-binary',
         'SIZE_UNIT_BINARY'),
        ('--size-unit-decimal',
         'SIZE_UNIT_DECIMAL'),
        'ARCHIVE_PATH+',
    ],
)
def task_list(runner: TzarTaskRunner):
    def _item_tuple(item: MethodListItem) -> Tuple[Text, Text, Text]:
        file_size = runner.format_size(item.size)
        file_time = strftime('%c', localtime(item.time))
        return file_size, file_time, item.path
    for archive_path in runner.args.ARCHIVE_PATH:
        archive_items = list_archive(archive_path)
        for line in format_table(*[_item_tuple(item) for item in archive_items],
                                 headers=['size', 'date/time', 'path']):
            print(line)
