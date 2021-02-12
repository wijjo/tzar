"""Tzar catalog command."""

import os
from typing import Tuple, Text, Iterator, List, Optional

import jiig
from jiig.util.general import format_table
from jiig.util.filesystem import short_path

from tzar.internal.archiver import CatalogItem, create_archiver, Archiver
from tzar.internal.constants import DEFAULT_ARCHIVE_FOLDER
from tzar.internal.utility import format_file_size


TASK = jiig.Task(
    description='Manage and view archive catalog folders.',

    args={
        'LONG_FORMAT[!]': ('-l', '--long',
                           'Long format to display extra information'),
        'AGE_MAX': ('--age-max',
                    'Maximum archive age [age_option]',
                    jiig.arg.str_to_age),
        'AGE_MIN': ('--age-min',
                    'Minimum archive age [age_option]',
                    jiig.arg.str_to_age),
        'ARCHIVE_FOLDER': ('-f', '--archive-folder',
                           'Archive folder',
                           jiig.arg.path_is_folder,
                           jiig.arg.path_to_absolute,
                           jiig.arg.default(DEFAULT_ARCHIVE_FOLDER)),
        'DATE_MAX': ('--date-max',
                     'Maximum (latest) archive date',
                     jiig.arg.str_to_timestamp),
        'DATE_MIN': ('--date-min',
                     'Minimum (earliest) archive date',
                     jiig.arg.str_to_timestamp),
        'INTERVAL_MAX': ('--interval-max',
                         'Maximum interval (n[HMS]) between saves to consider',
                         jiig.arg.str_to_interval),
        'INTERVAL_MIN': ('--interval-min',
                         'Minimum interval (n[HMS]) between saves to consider',
                         jiig.arg.str_to_interval),
        'SIZE_UNIT_BINARY[!]': ('--size-unit-binary',
                                'Format size as binary 1024-based KiB, MiB, etc.'),
        'SIZE_UNIT_DECIMAL[!]': ('--size-unit-decimal',
                                 'Format size as decimal 1000-based KB, MB, etc.'),
        'SOURCE_NAME': ('-n', '--name',
                        'Source name',
                        jiig.arg.default(os.path.basename(os.getcwd()))),
        'SOURCE_FOLDER': ('-s', '--source-folder',
                          'Source folder',
                          jiig.arg.path_is_folder,
                          jiig.arg.path_to_absolute,
                          jiig.arg.default('.')),
        'TAGS': ('-t', '--tags',
                 'Comma-separated archive tags',
                 jiig.arg.str_to_comma_tuple),
    },
)


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


@TASK.run
def task_run(runner: jiig.Runner, data: Data):
    archiver = create_archiver(data.SOURCE_FOLDER,
                               data.ARCHIVE_FOLDER,
                               source_name=data.SOURCE_NAME,
                               verbose=runner.verbose,
                               dry_run=runner.dry_run)
    print(f'''
::: {archiver.source_name} archive catalog from "{archiver.archive_folder}" :::
''')
    for line in format_table(*_get_rows(archiver, data),
                             headers=list(_get_headers(data))):
        print(line)


def _get_headers(data: Data) -> Iterator[Text]:
    yield 'date/time'
    yield 'method'
    yield 'tags'
    if data.LONG_FORMAT:
        yield 'size'
        yield 'file/folder name'


def _get_columns(item: CatalogItem, data: Data) -> Iterator[Text]:
    yield item.time_string
    yield item.method_name
    yield ','.join(item.tags)
    if data.LONG_FORMAT:
        yield format_file_size(item.size,
                               size_unit_binary=data.SIZE_UNIT_BINARY,
                               size_unit_decimal=data.SIZE_UNIT_DECIMAL)
        yield short_path(item.file_name, is_folder=os.path.isdir(item.path))


def _get_rows(archiver: Archiver, data: Data) -> Iterator[Tuple[Text]]:
    for item in archiver.list_catalog(
            date_min=data.DATE_MIN,
            date_max=data.DATE_MAX,
            age_min=data.AGE_MIN,
            age_max=data.AGE_MAX,
            interval_min=data.INTERVAL_MIN,
            interval_max=data.INTERVAL_MAX,
            tags=data.TAGS):
        yield list(_get_columns(item, data))
