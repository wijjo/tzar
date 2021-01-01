"""Tzar catalog command."""

import os
from typing import Tuple, Text, Iterator, List, Optional

from jiig import BoolOpt, Opt, adapters, Task
from jiig.utility.general import format_table
from jiig.utility.filesystem import short_path

from tzar.internal.archiver import CatalogItem, create_archiver, Archiver
from tzar.internal.constants import DEFAULT_ARCHIVE_FOLDER
from tzar.internal.utility import format_file_size


class TaskClass(Task):
    """Manage and view archive catalog folders."""

    # For type inspection only.
    class Data:
        LONG_FORMAT: bool
        AGE_MAX: Optional[float]
        AGE_MIN: Optional[float]
        ARCHIVE_FOLDER: Text
        DATE_MAX: Optional[float]
        DATE_MIN: Optional[float]
        INTERVAL_MAX: Optional[int]
        INTERVAL_MIN: Optional[int]
        SIZE_UNIT_BINARY: bool
        SIZE_UNIT_DECIMAL: bool
        SOURCE_NAME: Text
        SOURCE_FOLDER: Text
        TAGS: Optional[List[Text]]
    data: Data

    args = [
        BoolOpt(('-l', '--long'), 'LONG_FORMAT',
                'Long format to display extra information'),
        Opt('--age-max', 'AGE_MAX', 'Maximum archive age [age_option]',
            adapters.time.age),
        Opt('--age-min', 'AGE_MIN', 'Minimum archive age [age_option]',
            adapters.time.age),
        Opt(('-f', '--archive-folder'), 'ARCHIVE_FOLDER', 'Archive folder',
            adapters.path.check_folder,
            adapters.path.absolute,
            default_value=DEFAULT_ARCHIVE_FOLDER),
        Opt('--date-max', 'DATE_MAX', 'Maximum (latest) archive date',
            adapters.time.timestamp),
        Opt('--date-min', 'DATE_MIN', 'Minimum (earliest) archive date',
            adapters.time.timestamp),
        Opt('--interval-max', 'INTERVAL_MAX',
            'Maximum interval (n[HMS]) between saves to consider',
            adapters.time.interval),
        Opt('--interval-min', 'INTERVAL_MIN',
            'Minimum interval (n[HMS]) between saves to consider',
            adapters.time.interval),
        BoolOpt('--size-unit-binary', 'SIZE_UNIT_BINARY',
                'Format size as binary 1024-based KiB, MiB, etc.'),
        BoolOpt('--size-unit-decimal', 'SIZE_UNIT_DECIMAL',
                'Format size as decimal 1000-based KB, MB, etc.'),
        Opt(('-n', '--name'), 'SOURCE_NAME', 'Source name',
            default_value=os.path.basename(os.getcwd())),
        Opt(('-s', '--source-folder'), 'SOURCE_FOLDER', 'Source folder',
            adapters.path.check_folder,
            adapters.path.absolute,
            default_value='.'),
        Opt(('-t', '--tags'), 'TAGS', 'Comma-separated archive tags',
            adapters.text.comma_tuple),
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
            yield format_file_size(item.size,
                                   size_unit_binary=self.data.SIZE_UNIT_BINARY,
                                   size_unit_decimal=self.data.SIZE_UNIT_DECIMAL)
            yield short_path(item.file_name, is_folder=os.path.isdir(item.path))

    def _get_rows(self, archiver: Archiver) -> Iterator[Tuple[Text]]:
        for item in archiver.list_catalog(
                date_min=self.data.DATE_MIN,
                date_max=self.data.DATE_MAX,
                age_min=self.data.AGE_MIN,
                age_max=self.data.AGE_MAX,
                interval_min=self.data.INTERVAL_MIN,
                interval_max=self.data.INTERVAL_MAX,
                tags=self.data.TAGS):
            yield list(self._get_columns(item))

    def on_run(self):
        archiver = create_archiver(self.data.SOURCE_FOLDER,
                                   self.data.ARCHIVE_FOLDER,
                                   source_name=self.data.SOURCE_NAME,
                                   verbose=self.params.VERBOSE,
                                   dry_run=self.params.DRY_RUN)
        print(f'''
::: {archiver.source_name} archive catalog from "{archiver.archive_folder}" :::
''')
        for line in format_table(*self._get_rows(archiver),
                                 headers=list(self._get_headers())):
            print(line)
