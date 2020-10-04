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
        'INTERVAL_MAX',
        'INTERVAL_MIN',
        'SIZE_UNIT_BINARY',
        'SIZE_UNIT_DECIMAL',
        'SOURCE_NAME',
        'SOURCE_FOLDER',
        'TAGS',
    ],
)
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
