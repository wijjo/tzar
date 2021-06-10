"""Tzar catalog command."""

import os
from typing import Tuple, Text, Iterator

import jiig
from jiig.util.general import format_table
from jiig.util.filesystem import short_path

from tzar.internal.archiver import CatalogItem, create_archiver, Archiver
from tzar.internal.constants import DEFAULT_ARCHIVE_FOLDER
from tzar.internal.utility import format_file_size


class Task(jiig.Task):
    """Manage and view archive catalog folders."""

    long_format: jiig.boolean(
        'Long format to display extra information.',
        cli_flags=('-l', '--long'))

    age_max: jiig.age(
        'Maximum archive age [age_option].',
        cli_flags='--age-max')

    age_min: jiig.age(
        'Minimum archive age [age_option].',
        cli_flags='--age-min')

    date_max: jiig.timestamp(
        'Maximum (latest) archive date.',
        cli_flags='--date-max')

    date_min: jiig.timestamp(
        'Minimum (earliest) archive date.',
        cli_flags='--date-min')

    interval_max: jiig.interval(
        'Maximum interval (n[HMS]) between saves to consider.',
        cli_flags='--interval-max')

    interval_min: jiig.interval(
        'Minimum interval (n[HMS]) between saves to consider.',
        cli_flags='--interval-min')

    size_unit_binary: jiig.boolean(
        'Format size as binary 1024-based KiB, MiB, etc..',
        cli_flags='--size-unit-binary')

    size_unit_decimal: jiig.boolean(
        'Format size as decimal 1000-based KB, MB, etc..',
        cli_flags='--size-unit-decimal')

    tags: jiig.comma_tuple(
        'Comma-separated archive tags.',
        cli_flags=('-t', '--tags'))

    archive_folder: jiig.filesystem_folder(
        'Archive folder.',
        absolute_path=True,
        cli_flags=('-f', '--archive-folder')
    ) = DEFAULT_ARCHIVE_FOLDER

    source_name: jiig.text(
        'Source name.',
        cli_flags=('-n', '--name')
    ) = os.path.basename(os.getcwd())

    source_folder: jiig.filesystem_folder(
        'Source folder.',
        absolute_path=True,
        cli_flags=('-s', '--source-folder')
    ) = '.'

    def on_run(self, runtime: jiig.Runtime):
        archiver = create_archiver(self.source_folder,
                                   self.archive_folder,
                                   source_name=self.source_name,
                                   verbose=runtime.options.verbose,
                                   dry_run=runtime.options.dry_run)
        print(f'''
::: {archiver.source_name} archive catalog from "{archiver.archive_folder}" :::
''')
        for line in format_table(*self._get_rows(archiver),
                                 headers=list(self._get_headers())):
            print(line)

    def _get_headers(self) -> Iterator[Text]:
        yield 'date/time'
        yield 'method'
        yield 'tags'
        if self.long_format:
            yield 'size'
            yield 'file/folder name'

    def _get_columns(self, item: CatalogItem) -> Iterator[Text]:
        yield item.time_string
        yield item.method_name
        yield ','.join(item.tags)
        if self.long_format:
            yield format_file_size(item.size,
                                   size_unit_binary=self.size_unit_binary,
                                   size_unit_decimal=self.size_unit_decimal)
            yield short_path(item.file_name, is_folder=os.path.isdir(item.path))

    def _get_rows(self, archiver: Archiver) -> Iterator[Tuple[Text]]:
        for item in archiver.list_catalog(
                date_min=self.date_min,
                date_max=self.date_max,
                age_min=self.age_min,
                age_max=self.age_max,
                interval_min=self.interval_min,
                interval_max=self.interval_max,
                tags=self.tags):
            yield list(self._get_columns(item))
