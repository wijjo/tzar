"""Tzar catalog command."""

import os
from typing import Tuple, Text, Iterator

from jiig import task
from jiig.utility.general import format_table
from jiig.utility.filesystem import short_path

from tzar.internal.archiver import CatalogItem
from tzar.internal.task_runner import TzarTaskRunner
from .arguments import long_format_argument, age_max_argument, age_min_argument, archive_folder_argument, \
    date_max_argument, date_min_argument, interval_max_argument, interval_min_argument, \
    size_unit_binary_argument, size_unit_decimal_argument, source_name_argument, source_folder_argument, tags_argument


@task('catalog',
      long_format_argument(),
      age_max_argument(),
      age_min_argument(),
      archive_folder_argument(),
      date_max_argument(),
      date_min_argument(),
      interval_max_argument(),
      interval_min_argument(),
      size_unit_binary_argument(),
      size_unit_decimal_argument(),
      source_name_argument(),
      source_folder_argument(),
      tags_argument(),
      description='Manage and view archive catalog folders')
def task_catalog(runner: TzarTaskRunner):

    def _get_headers() -> Iterator[Text]:
        yield 'date/time'
        yield 'method'
        yield 'tags'
        if runner.args.LONG_FORMAT:
            yield 'size'
            yield 'file/folder name'

    def _get_columns(item: CatalogItem) -> Iterator[Text]:
        yield item.time_string
        yield item.method_name
        yield ','.join(item.tags)
        if runner.args.LONG_FORMAT:
            yield runner.format_size(item.size)
            yield short_path(item.file_name, is_folder=os.path.isdir(item.path))

    def _get_rows() -> Iterator[Tuple[Text]]:
        for item in runner.list_catalog():
            yield list(_get_columns(item))

    print(f'''
::: {runner.source_name} archive catalog from "{runner.archive_folder}" :::
''')
    for line in format_table(*_get_rows(), headers=list(_get_headers())):
        print(line)
