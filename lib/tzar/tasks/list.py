"""Tzar list command."""

from time import localtime, strftime
from typing import Text, Tuple

from jiig.utility.general import format_table

from tzar.internal.archiver import MethodListItem
from tzar.internal.tzar_task import TzarTask
from tzar.internal.archiver import list_archive

from . import arguments


class TaskClass(TzarTask):
    """List archive contents."""

    opts = [
        arguments.size_unit_binary_option(),
        arguments.size_unit_decimal_option(),
    ]
    args = [
        arguments.archive_path_argument(cardinality='+'),
    ]

    def on_run(self):
        def _item_tuple(item: MethodListItem) -> Tuple[Text, Text, Text]:
            file_size = self.format_size(item.size)
            file_time = strftime('%c', localtime(item.time))
            return file_size, file_time, item.path
        for archive_path in self.data.ARCHIVE_PATH:
            archive_items = list_archive(archive_path)
            for line in format_table(*[_item_tuple(item) for item in archive_items],
                                     headers=['size', 'date/time', 'path']):
                print(line)
