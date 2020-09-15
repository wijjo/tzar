"""Tzar list command."""

from time import localtime, strftime
from typing import Text, Tuple

from jiig import task, TaskRunner
from jiig.utility.general import format_table, format_byte_count

from tzar.archiver import Archiver
from tzar.methods.base import MethodListItem


@task(
    'list',
    help='list archive contents',
    options={
        ('-S', '--size-format'): {
            'dest': 'SIZE_FORMAT',
            'choices': ['b', 'd'],
            'help': 'format size as decimal KB/MB/... if "d" or binary KiB/MiB if "b"',
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
            file_size = format_byte_count(item.size, unit_format=runner.args.SIZE_FORMAT)
        else:
            file_size = '-'
        file_time = strftime('%c', localtime(item.time))
        return file_size, file_time, item.path
    archiver = Archiver()
    for archive_path in runner.args.SOURCE_ARCHIVE:
        archive_items = archiver.list_archive(archive_path)
        for line in format_table(*[_item_tuple(item) for item in archive_items],
                                 headers=['size', 'date/time', 'path']):
            print(line)
