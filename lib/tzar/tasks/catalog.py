"""Tzar catalog command."""

import os
from typing import Tuple, Text, Iterator, List, Optional

import jiig
from jiig.utility.general import format_table
from jiig.utility.filesystem import short_path

from tzar.internal.archiver import CatalogItem, create_archiver, Archiver
from tzar.internal.constants import DEFAULT_ARCHIVE_FOLDER
from tzar.internal.utility import format_file_size


class TaskClass(jiig.Task):
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

    args = {
        'LONG_FORMAT!': ('-l', '--long',
                         'Long format to display extra information'),
        'AGE_MAX': ('--age-max',
                    'Maximum archive age [age_option]',
                    jiig.time.age),
        'AGE_MIN': ('--age-min',
                    'Minimum archive age [age_option]',
                    jiig.time.age),
        'ARCHIVE_FOLDER': ('-f', '--archive-folder',
                           'Archive folder',
                           jiig.path.check_folder,
                           jiig.path.absolute,
                           jiig.Default(DEFAULT_ARCHIVE_FOLDER)),
        'DATE_MAX': ('--date-max',
                     'Maximum (latest) archive date',
                     jiig.time.timestamp),
        'DATE_MIN': ('--date-min',
                     'Minimum (earliest) archive date',
                     jiig.time.timestamp),
        'INTERVAL_MAX': ('--interval-max',
                         'Maximum interval (n[HMS]) between saves to consider',
                         jiig.time.interval),
        'INTERVAL_MIN': ('--interval-min',
                         'Minimum interval (n[HMS]) between saves to consider',
                         jiig.time.interval),
        'SIZE_UNIT_BINARY!': ('--size-unit-binary',
                              'Format size as binary 1024-based KiB, MiB, etc.'),
        'SIZE_UNIT_DECIMAL!': ('--size-unit-decimal',
                               'Format size as decimal 1000-based KB, MB, etc.'),
        'SOURCE_NAME': ('-n', '--name',
                        'Source name',
                        jiig.Default(os.path.basename(os.getcwd()))),
        'SOURCE_FOLDER': ('-s', '--source-folder',
                          'Source folder',
                          jiig.path.check_folder,
                          jiig.path.absolute,
                          jiig.Default('.')),
        'TAGS': ('-t', '--tags',
                 'Comma-separated archive tags',
                 jiig.text.comma_tuple),
    }

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
