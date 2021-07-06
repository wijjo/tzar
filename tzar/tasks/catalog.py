"""Tzar catalog command."""

import os
from typing import Tuple, Text, Iterator

import jiig
from jiig.util.general import format_table
from jiig.util.filesystem import short_path

from tzar import arguments
from tzar.runtime import TzarRuntime, CatalogItem
from tzar.utility import format_file_size


@jiig.task
def catalog(
    runtime: TzarRuntime,
    long_format: arguments.long_format_option,
    age_max: arguments.age_max_option,
    age_min: arguments.age_min_option,
    date_max: arguments.date_max_option,
    date_min: arguments.date_min_option,
    interval_max: arguments.interval_max_option,
    interval_min: arguments.interval_min_option,
    size_unit_binary: arguments.size_unit_binary_option,
    size_unit_decimal: arguments.size_unit_decimal_option,
    tags: arguments.tags_option,
    archive_folder: arguments.archive_folder_option,
    source_name: arguments.source_name_option,
    source_folder: arguments.source_folder_option,
):
    """Manage and view archive catalog folders."""
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
            yield short_path(item.file_name, is_folder=os.path.isdir(item.path))

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
