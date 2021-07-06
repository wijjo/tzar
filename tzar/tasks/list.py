"""Tzar list command."""

from time import localtime, strftime
from typing import Text, Tuple

import jiig
from jiig.util.general import format_table

from tzar import arguments
from tzar.archive_method import MethodListItem
from tzar.runtime import TzarRuntime
from tzar.utility import format_file_size


# Trailing underscore avoids conflict with built-in list type, while still
# serving as default task name, since the underscore is automatically dropped.
@jiig.task
def list_(
    runtime: TzarRuntime,
    size_unit_binary: arguments.size_unit_binary_option,
    size_unit_decimal: arguments.size_unit_decimal_option,
    archive_path: arguments.archive_paths_argument,
):
    """List archive contents."""

    def _item_tuple(item: MethodListItem) -> Tuple[Text, Text, Text]:
        file_size = format_file_size(item.size,
                                     size_unit_binary=size_unit_binary,
                                     size_unit_decimal=size_unit_decimal)
        file_time = strftime('%c', localtime(item.time))
        return file_size, file_time, item.path

    for archive_path_item in archive_path:
        archive_items = runtime.list_archive(archive_path_item)
        for line in format_table(*[_item_tuple(item) for item in archive_items],
                                 headers=['size', 'date/time', 'path']):
            print(line)
