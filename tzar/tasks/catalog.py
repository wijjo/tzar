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

"""Tzar catalog command."""

import os
from typing import Tuple, Text, Iterator

import jiig
from jiig.util.filesystem import short_path
from jiig.util.text.table import format_table

from tzar import constants
from tzar.runtime import TzarRuntime, CatalogItem
from tzar.utility import format_file_size


@jiig.task(
    cli={
        'options': {
            'long_format': constants.OPTION_LONG_FORMAT,
            'age_min': constants.OPTION_AGE_MIN,
            'age_max': constants.OPTION_AGE_MAX,
            'date_min': constants.OPTION_DATE_MIN,
            'date_max': constants.OPTION_DATE_MAX,
            'interval_max': constants.OPTION_INTERVAL_MAX,
            'interval_min': constants.OPTION_INTERVAL_MIN,
            'size_unit_binary': constants.OPTION_SIZE_UNIT_BINARY,
            'size_unit_decimal': constants.OPTION_SIZE_UNIT_DECIMAL,
            'tags': constants.OPTION_TAGS,
            'archive_folder': constants.OPTION_ARCHIVE_FOLDER,
            'source_name': constants.OPTION_SOURCE_NAME,
            'source_folder': constants.OPTION_SOURCE_FOLDER,
        }
    }
)
def catalog(
    runtime: TzarRuntime,
    long_format: jiig.f.boolean(),
    age_max: jiig.f.age(),
    age_min: jiig.f.age(),
    date_max: jiig.f.timestamp(),
    date_min: jiig.f.timestamp(),
    interval_max: jiig.f.interval(),
    interval_min: jiig.f.interval(),
    size_unit_binary: jiig.f.boolean(),
    size_unit_decimal: jiig.f.boolean(),
    tags: jiig.f.comma_list(),
    archive_folder: jiig.f.filesystem_folder(absolute_path=True) = constants.DEFAULT_ARCHIVE_FOLDER,
    source_name: jiig.f.text() = os.path.basename(os.getcwd()),
    source_folder: jiig.f.filesystem_folder(absolute_path=True) = '.',
):
    """
    Manage and view archive catalog folders.

    :param runtime: Jiig runtime API.
    :param long_format: Long format to display extra information.
    :param age_max: Maximum archive age [^age_option].
    :param age_min: Minimum archive age [^age_option].
    :param date_max: Maximum (latest) archive date.
    :param date_min: Minimum (earliest) archive date.
    :param interval_max: Maximum interval (n[HMS]) between saves to consider.
    :param interval_min: Minimum interval (n[HMS]) between saves to consider.
    :param size_unit_binary: Format size as binary 1024-based KiB, MiB, etc..
    :param size_unit_decimal: Format size as decimal 1000-based KB, MB, etc..
    :param tags: Comma-separated archive tags.
    :param archive_folder: Archive folder.
    :param source_name: Source name.
    :param source_folder: Source folder.
    """
    def _get_headers() -> Iterator[Text]:
        yield 'date/time'
        yield 'method'
        yield 'tags'
        if long_format:
            yield 'size'
            yield 'file/folder name'

    def _get_columns(item: CatalogItem) -> Iterator[Text]:
        yield item.time_string
        yield item.method_name
        yield ','.join(item.tags)
        if long_format:
            yield format_file_size(item.size,
                                   size_unit_binary=size_unit_binary,
                                   size_unit_decimal=size_unit_decimal)
            yield short_path(item.path.name, is_folder=os.path.isdir(item.path))

    def _get_rows() -> Iterator[Tuple[Text]]:
        for item in runtime.list_catalog(
                source_folder,
                archive_folder,
                source_name=source_name,
                date_min=date_min,
                date_max=date_max,
                age_min=age_min,
                age_max=age_max,
                interval_min=interval_min,
                interval_max=interval_max,
                tags=tags):
            yield list(_get_columns(item))

    with runtime.context(source_name=source_name,
                         archive_folder=archive_folder,
                         ) as context:
        context.heading(1, '{source_name} archive catalog from "{archive_folder}"')
        for line in format_table(*_get_rows(), headers=list(_get_headers())):
            print(line)
