"""Tzar catalog command."""

import os
from typing import Tuple, Text, Iterator

from jiig.utility.general import format_table
from jiig.utility.filesystem import short_path

from tzar.internal.archiver import CatalogItem
from tzar.internal.tzar_task import TzarTask

from . import arguments


class TaskClass(TzarTask):
    """Manage and view archive catalog folders."""

    opts = [
        arguments.long_format_option(),
        arguments.age_max_option(),
        arguments.age_min_option(),
        arguments.archive_folder_option(),
        arguments.date_max_option(),
        arguments.date_min_option(),
        arguments.interval_max_option(),
        arguments.interval_min_option(),
        arguments.size_unit_binary_option(),
        arguments.size_unit_decimal_option(),
        arguments.source_name_option(),
        arguments.source_folder_option(),
        arguments.tags_option(),
    ]

    def _get_headers(self) -> Iterator[Text]:
        yield 'date/time'
        yield 'method'
        yield 'tags'
        if self.data.LONG_FORMAT:
            yield 'size'
            yield 'file/folder name'

    def _get_columns(self, item: CatalogItem) -> Iterator[Text]:
        yield item.time_string
        yield item.method_name
        yield ','.join(item.tags)
        if self.data.LONG_FORMAT:
            yield self.format_size(item.size)
            yield short_path(item.file_name, is_folder=os.path.isdir(item.path))

    def _get_rows(self) -> Iterator[Tuple[Text]]:
        for item in self.list_catalog():
            yield list(self._get_columns(item))

    def on_run(self):
        print(f'''
::: {self.source_name} archive catalog from "{self.archive_folder}" :::
''')
        for line in format_table(*self._get_rows(), headers=list(self._get_headers())):
            print(line)
