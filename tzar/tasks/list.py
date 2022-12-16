# Copyright (C) 2021-2022, Steven Cooper
#
# This file is part of Tzar.
#
# Tzar is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Tzar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Tzar.  If not, see <https://www.gnu.org/licenses/>.

"""Tzar list command."""

from time import localtime, strftime

import jiig
from jiig.util.text.table import format_table

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

    def _item_tuple(item: MethodListItem) -> tuple[str, str, str]:
        file_size = format_file_size(item.size,
                                     size_unit_binary=size_unit_binary,
                                     size_unit_decimal=size_unit_decimal)
        file_time = strftime('%c', localtime(item.time))
        return file_size, file_time, str(item.path)

    for archive_path_item in archive_paths:
        archive_items = runtime.list_archive(archive_path_item)
        for line in format_table(*[_item_tuple(item) for item in archive_items],
                                 headers=['size', 'date/time', 'path']):
            print(line)
