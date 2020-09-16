"""Tzar list command."""

from time import localtime, strftime
from typing import Text, Tuple

from jiig import task
from jiig.utility.general import format_table

from tzar import TzarTaskRunner, MethodListItem


@task(
    'list',
    help='list archive contents',
    common_options=['BINARY_SIZE_UNIT', 'DECIMAL_SIZE_UNIT'],
    common_arguments=['SOURCE_ARCHIVE+']
)
def task_list(runner: TzarTaskRunner):
    def _item_tuple(item: MethodListItem) -> Tuple[Text, Text, Text]:
        file_size = runner.format_size(item.size)
        file_time = strftime('%c', localtime(item.time))
        return file_size, file_time, item.path
    archiver = runner.create_archiver()
    for archive_path in runner.args.SOURCE_ARCHIVE:
        archive_items = archiver.list_archive(archive_path)
        for line in format_table(*[_item_tuple(item) for item in archive_items],
                                 headers=['size', 'date/time', 'path']):
            print(line)
