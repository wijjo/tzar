"""Tzar catalog command."""

import os
from typing import Tuple, Text, Iterator

from jiig import task, TaskRunner
from jiig.utility.general import format_table, format_byte_count
from jiig.utility.filesystem import short_path

from tzar.archiver import create_archiver, CatalogItem
from tzar.constants import DEFAULT_ARCHIVE_FOLDER


@task(
    'catalog',
    help='manage and view archive catalog folders',
    options={
        ('-l', '--long'): {
            'dest': 'LONG_FORMAT',
            'action': 'store_true',
            'help': 'long format to display extra information',
        },
        ('-s', '--source-folder'): {
            'dest': 'SOURCE_FOLDER',
            'help': 'source folder (default: working folder)',
        },
        ('-n', '--name'): {
            'dest': 'SOURCE_NAME',
            'help': 'source name (default: working folder name)',
        },
        ('-S', '--size-format'): {
            'dest': 'SIZE_FORMAT',
            'choices': ['b', 'd'],
            'help': 'format size as decimal KB/MB/... if "d" or binary KiB/MiB if "b"',
        },
    },
    arguments=[
        {
            'dest': 'ARCHIVE_FOLDER',
            'nargs': '?',
            'default': DEFAULT_ARCHIVE_FOLDER,
            'help': f'archive folder (default: "{DEFAULT_ARCHIVE_FOLDER}")',
        },
    ],
)
def task_catalog(runner: TaskRunner):
    archiver = create_archiver(source_name=runner.args.SOURCE_NAME, archive_folder=runner.args.ARCHIVE_FOLDER,
                               verbose=runner.verbose, dry_run=runner.dry_run)

    def _get_headers() -> Iterator[Text]:
        yield 'date/time'
        yield 'method'
        yield 'labels'
        if runner.args.LONG_FORMAT:
            yield 'size'
            yield 'file/folder name'

    def _get_columns(item: CatalogItem) -> Iterator[Text]:
        yield item.time_string
        yield item.method_name
        yield ','.join(item.labels)
        if runner.args.LONG_FORMAT:
            if item.size is not None:
                yield format_byte_count(item.size, unit_format=runner.args.SIZE_FORMAT)
            else:
                yield '-'
            yield short_path(item.file_name, is_folder=os.path.isdir(item.file_path))

    def _get_rows() -> Iterator[Tuple[Text]]:
        for item in archiver.list_catalog(runner.args.SOURCE_FOLDER):
            yield list(_get_columns(item))

    for line in format_table(*_get_rows(), headers=list(_get_headers())):
        print(line)
