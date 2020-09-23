"""Tzar catalog command."""

import os
from typing import Tuple, Text, Iterator

from jiig import task
from jiig.utility.general import format_table
from jiig.utility.filesystem import short_path

from tzar import TzarTaskRunner, CatalogItem


@task(
    'catalog',
    help='manage and view archive catalog folders',
    options={
        ('-l', '--long'): {
            'dest': 'LONG_FORMAT',
            'action': 'store_true',
            'help': 'long format to display extra information',
        },
    },
    common_options=[
        'AGE_MAX',
        'AGE_MIN',
        'ARCHIVE_FOLDER',
        'DATE_MAX',
        'DATE_MIN',
        'SIZE_UNIT_BINARY',
        'SIZE_UNIT_DECIMAL',
        'SOURCE_NAME',
        'SOURCE_FOLDER',
        'TAGS',
    ],
)
def task_catalog(runner: TzarTaskRunner):
    archiver = runner.create_archiver(source_name=runner.args.SOURCE_NAME,
                                      archive_folder=runner.args.ARCHIVE_FOLDER)

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
            yield short_path(item.file_name, is_folder=os.path.isdir(item.file_path))

    def _get_rows() -> Iterator[Tuple[Text]]:
        for item in archiver.list_catalog(runner.args.SOURCE_FOLDER,
                                          timestamp_min=runner.timestamp_min,
                                          timestamp_max=runner.timestamp_max,
                                          tags=runner.tags):
            yield list(_get_columns(item))

    for line in format_table(*_get_rows(), headers=list(_get_headers())):
        print(line)
