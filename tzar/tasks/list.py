"""Tzar list command."""

from time import localtime, strftime
from typing import Text, Tuple

import jiig
from jiig.util.general import format_table

from tzar import constants
from tzar.archive_method import MethodListItem
from tzar.runtime import TzarRuntime
from tzar.utility import format_file_size


# Trailing underscore avoids conflict with built-in list type, while still
# serving as default task name, since the underscore is automatically dropped.
@jiig.task(
    cli={
        'options': {
            'size_unit_binary': constants.OPTION_SIZE_UNIT_BINARY,
            'size_unit_decimal': constants.OPTION_SIZE_UNIT_DECIMAL,
        }
    }
)
def list_(
    runtime: TzarRuntime,
    size_unit_binary: jiig.f.boolean(),
    size_unit_decimal: jiig.f.boolean(),
    archive_paths: jiig.f.filesystem_object(exists=True, repeat=(1, None)),
):
    """
    List archive contents.

    :param runtime: Jiig runtime API.
    :param size_unit_binary: Format size as binary 1024-based KiB, MiB, etc..
    :param size_unit_decimal: Format size as decimal 1000-based KB, MB, etc..
    :param archive_paths: Path(s) to source archive file or folder.
    """

    def _item_tuple(item: MethodListItem) -> Tuple[Text, Text, Text]:
        file_size = format_file_size(item.size,
                                     size_unit_binary=size_unit_binary,
                                     size_unit_decimal=size_unit_decimal)
        file_time = strftime('%c', localtime(item.time))
        return file_size, file_time, item.path

    for archive_path_item in archive_paths:
        archive_items = runtime.list_archive(archive_path_item)
        for line in format_table(*[_item_tuple(item) for item in archive_items],
                                 headers=['size', 'date/time', 'path']):
            print(line)
