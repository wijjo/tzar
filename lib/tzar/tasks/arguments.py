"""Tzar common arguments and options."""

import os

import jiig

from tzar.methods import DEFAULT_METHOD
from tzar.internal.archiver import get_method_names
from tzar.internal.constants import DEFAULT_ARCHIVE_FOLDER


def age_max_option() -> jiig.Opt:
    return jiig.Opt('--age-max', 'AGE_MAX', 'Maximum archive age [age_option]',
                    jiig.adapters.time.age)


def age_min_option() -> jiig.Opt:
    return jiig.Opt('--age-min', 'AGE_MIN', 'Minimum archive age [age_option]',
                    jiig.adapters.time.age)


def archive_folder_option() -> jiig.Opt:
    return jiig.Opt(('-f', '--archive-folder'), 'ARCHIVE_FOLDER', 'Archive folder',
                    jiig.adapters.path.check_folder,
                    default_value=DEFAULT_ARCHIVE_FOLDER)


def archive_path_argument(cardinality: jiig.Cardinality = None) -> jiig.Arg:
    return jiig.Arg('ARCHIVE_PATH', 'Path to source archive file or folder',
                    jiig.adapters.path.check_exists,
                    cardinality=cardinality)


def archive_path_option(cardinality: jiig.Cardinality = None) -> jiig.Opt:
    return jiig.Opt(('-p', '--archive-path'), 'ARCHIVE_PATH',
                    'Path to source archive file or folder',
                    jiig.adapters.path.check_exists,
                    cardinality=cardinality)


def date_max_option() -> jiig.Opt:
    return jiig.Opt('--date-max', 'DATE_MAX', 'Maximum (latest) archive date',
                    jiig.adapters.time.timestamp)


def date_min_option() -> jiig.Opt:
    return jiig.Opt('--date-min', 'DATE_MIN', 'Minimum (earliest) archive date',
                    jiig.adapters.time.timestamp)


def interval_max_option() -> jiig.Opt:
    return jiig.Opt('--interval-max', 'INTERVAL_MAX',
                    'Maximum interval (n[HMS]) between saves to consider',
                    jiig.adapters.time.interval)


def interval_min_option() -> jiig.Opt:
    return jiig.Opt('--interval-min', 'INTERVAL_MIN',
                    'Minimum interval (n[HMS]) between saves to consider',
                    jiig.adapters.time.interval)


def long_format_option() -> jiig.BoolOpt:
    return jiig.BoolOpt(('-l', '--long'), 'LONG_FORMAT',
                        'Long format to display extra information')


def method_option() -> jiig.Opt:
    return jiig.Opt(('-m', '--method'), 'METHOD', 'Archive method',
                    default_value=DEFAULT_METHOD,
                    choices=get_method_names())


def no_confirmation_option() -> jiig.BoolOpt:
    return jiig.BoolOpt('--no-confirmation', 'NO_CONFIRMATION',
                        'Execute destructive actions without prompting for confirmation')


def size_unit_binary_option() -> jiig.BoolOpt:
    return jiig.BoolOpt('--size-unit-binary', 'SIZE_UNIT_BINARY',
                        'Format size as binary 1024-based KiB, MiB, etc.')


def size_unit_decimal_option() -> jiig.BoolOpt:
    return jiig.BoolOpt('--size-unit-decimal', 'SIZE_UNIT_DECIMAL',
                        'Format size as decimal 1000-based KB, MB, etc.')


def source_folder_option(cardinality: jiig.Cardinality = None) -> jiig.Opt:
    return jiig.Opt(('-s', '--source-folder'), 'SOURCE_FOLDER', 'Source folder',
                    jiig.adapters.path.check_folder,
                    default_value='.',
                    cardinality=cardinality)


def source_name_option() -> jiig.Opt:
    return jiig.Opt(('-n', '--name'), 'SOURCE_NAME', 'Source name',
                    default_value=os.path.basename(os.getcwd()))


def tags_option() -> jiig.Opt:
    return jiig.Opt(('-t', '--tags'), 'TAGS', 'Comma-separated archive tags',
                    jiig.adapters.text.comma_tuple)
