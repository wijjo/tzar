"""Tzar list command."""

from time import localtime, strftime
from typing import Text, Tuple

from jiig import task, TaskRunner
from jiig.utility.general import format_table, format_byte_count

from tzar.archiver import list_archive
from tzar.methods.base import MethodListItem


@task(
    'list',
    help='list archive contents',
    options={
        ('-u', '--decimal-units'): {
            'dest': 'DECIMAL_UNITS',
            'action': 'store_true',
            'help': 'display sizes as decimal, e.g. KB, MB, units',
        },
        ('-U', '--binary-units'): {
            'dest': 'BINARY_UNITS',
            'action': 'store_true',
            'help': 'display sizes as binary, e.g. KiB, MiB, units',
        },
    },
    arguments=[
        {
            'dest': 'SOURCE_ARCHIVE',
            'nargs': '+',
            'help': 'source archive file or folder',
        },
    ],
)
def task_list(runner: TaskRunner):
    def _item_tuple(item: MethodListItem) -> Tuple[Text, Text, Text]:
        if item.size is not None:
            if runner.args.DECIMAL_UNITS:
                file_size = format_byte_count(item.size)
            elif runner.args.BINARY_UNITS:
                file_size = format_byte_count(item.size, binary_units=True)
            else:
                file_size = str(item.size)
        else:
            file_size = '-'
        file_time = strftime('%c', localtime(item.time))
        return file_size, file_time, item.path
    for archive_path in runner.args.SOURCE_ARCHIVE:
        archive_items = list_archive(archive_path)
        for line in format_table(*[_item_tuple(item) for item in archive_items],
                                 headers=['size', 'date/time', 'path']):
            print(line)
