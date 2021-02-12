"""Tzar list command."""

from time import localtime, strftime
from typing import Text, Tuple, List

import jiig
from jiig.util.general import format_table

from tzar.internal.utility import format_file_size
from tzar.internal.archiver import MethodListItem
from tzar.internal.archiver import list_archive


TASK = jiig.Task(
    description='List archive contents.',
    args={
        'SIZE_UNIT_BINARY[!]': ('--size-unit-binary',
                                'Format size as binary 1024-based KiB, MiB, etc.'),
        'SIZE_UNIT_DECIMAL[!]': ('--size-unit-decimal',
                                 'Format size as decimal 1000-based KB, MB, etc.'),
        'ARCHIVE_PATH[+]': ('Path to source archive file or folder',
                            jiig.arg.path_exists),
    },
)


# For type inspection only.
class Data:
    SIZE_UNIT_BINARY: bool
    SIZE_UNIT_DECIMAL: bool
    ARCHIVE_PATH: List[Text]


@TASK.run
def task_run(_runner: jiig.Runner, data: Data):
    def _item_tuple(item: MethodListItem) -> Tuple[Text, Text, Text]:
        file_size = format_file_size(item.size,
                                     size_unit_binary=data.SIZE_UNIT_BINARY,
                                     size_unit_decimal=data.SIZE_UNIT_DECIMAL)
        file_time = strftime('%c', localtime(item.time))
        return file_size, file_time, item.path

    for archive_path in data.ARCHIVE_PATH:
        archive_items = list_archive(archive_path)
        for line in format_table(*[_item_tuple(item) for item in archive_items],
                                 headers=['size', 'date/time', 'path']):
            print(line)
