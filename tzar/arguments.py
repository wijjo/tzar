"""Tzar common arguments and options."""

import os

import jiig

from .constants import DEFAULT_ARCHIVE_FOLDER
from .methods import DEFAULT_METHOD
from .runtime import TzarRuntime

archive_folder_option = jiig.filesystem_folder(
    'Archive folder.',
    absolute_path=True,
    cli_flags=('-f', '--archive-folder'),
    default=DEFAULT_ARCHIVE_FOLDER,
)

source_name_option = jiig.text(
    'Source name.',
    cli_flags=('-n', '--name'),
    default=os.path.basename(os.getcwd()),
)

source_folder_option = jiig.filesystem_folder(
    'Source folder.',
    absolute_path=True,
    cli_flags=('-s', '--source-folder'),
    default='.',
)

method_option = jiig.text(
    'Archive method.',
    cli_flags=('-m', '--method'),
    choices=TzarRuntime.get_method_names(),
    default=DEFAULT_METHOD,
)

tags_option = jiig.comma_tuple(
    'Comma-separated archive tags.',
    cli_flags=('-t', '--tags'),
)

archive_path_argument = jiig.filesystem_object(
    f'Path to source archive file or folder.',
    exists=True,
)

archive_paths_argument = jiig.filesystem_object(
    f'Path(s) to source archive file or folder.',
    exists=True,
    repeat=(1, None),
)

size_unit_binary_option = jiig.boolean(
    'Format size as binary 1024-based KiB, MiB, etc..',
    cli_flags='--size-unit-binary',
)

size_unit_decimal_option = jiig.boolean(
    'Format size as decimal 1000-based KB, MB, etc..',
    cli_flags='--size-unit-decimal',
)

long_format_option = jiig.boolean(
    'Long format to display extra information.',
    cli_flags=('-l', '--long'),
)

age_max_option = jiig.age(
    'Maximum archive age [age_option].',
    cli_flags='--age-max',
)

age_min_option = jiig.age(
    'Minimum archive age [age_option].',
    cli_flags='--age-min',
)

date_max_option = jiig.timestamp(
    'Maximum (latest) archive date.',
    cli_flags='--date-max',
)

date_min_option = jiig.timestamp(
    'Minimum (earliest) archive date.',
    cli_flags='--date-min',
)

interval_max_option = jiig.interval(
    'Maximum interval (n[HMS]) between saves to consider.',
    cli_flags='--interval-max',
)

interval_min_option = jiig.interval(
    'Minimum interval (n[HMS]) between saves to consider.',
    cli_flags='--interval-min',
)

no_confirmation_option = jiig.boolean(
    'Execute destructive actions without prompting for confirmation.',
    cli_flags='--no-confirmation',
)

exclude_option = jiig.text(
    'Exclusion pattern(s), including gitignore-style wildcards.',
    repeat=None,
    cli_flags=('-e', '--exclude'),
)

progress_option = jiig.boolean(
    'Display progress statistics.',
    cli_flags=('-p', '--progress'),
)

disable_timestamp_option = jiig.boolean(
    'Disable adding timestamp to name.',
    cli_flags=('-T', '--no-timestamp'),
)

gitignore_option = jiig.boolean(
    'Use .gitignore exclusions.',
    cli_flags='--gitignore',
)

keep_list_option = jiig.boolean(
    'Do not delete temporary file list when done.',
    cli_flags='--keep-list',
)

pending_option = jiig.boolean(
    'Save only modified version-controlled files.',
    cli_flags='--pending',
)
