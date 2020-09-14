"""Tzar catalog command."""

from typing import Iterable, Tuple, Text

from jiig import task, TaskRunner
from jiig.utility.general import format_table

from tzar.archiver import create_archiver, Archiver
from tzar.constants import DEFAULT_ARCHIVE_FOLDER


@task(
    'catalog',
    help='manage and view archive catalog folders',
    options={
        ('-s', '--source-folder'): {
            'dest': 'SOURCE_FOLDER',
            'help': 'source folder (default: working folder)',
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
    archiver = create_archiver(archive_folder=runner.args.ARCHIVE_FOLDER,
                               verbose=runner.verbose,
                               dry_run=runner.dry_run)
    for line in format_table(*_get_rows(archiver, runner.args.SOURCE_FOLDER),
                             headers=['date/time', 'method', 'comment']):
        print(line)


def _get_rows(archiver: Archiver, source_folder: Text) -> Iterable[Tuple]:
    for item in archiver.list_catalog(source_folder):
        yield item.time_string, item.method_name, item.comment
