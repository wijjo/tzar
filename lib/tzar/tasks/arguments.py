import os

import jiig

from tzar.internal.archiver import get_method_names, DEFAULT_METHOD
from tzar.internal.constants import DEFAULT_ARCHIVE_FOLDER


def age_max_option() -> jiig.Argument:
    return jiig.option('AGE_MAX',
                       '--age-max',
                       int,
                       description='Maximum archive age [age_option]')


def age_min_option() -> jiig.Argument:
    return jiig.option('AGE_MIN',
                       '--age-min',
                       int,
                       description='Minimum archive age [age_option]')


def archive_folder_option() -> jiig.Argument:
    return jiig.option('ARCHIVE_FOLDER',
                       ('-f', '--archive-folder'),
                       jiig.adapters.folder_path,
                       description='Archive folder',
                       default_value=DEFAULT_ARCHIVE_FOLDER)


def archive_path_argument(cardinality: jiig.Cardinality = None) -> jiig.Argument:
    return jiig.argument('ARCHIVE_PATH',
                         jiig.adapters.existing_path,
                         description='Path to source archive file or folder',
                         cardinality=cardinality)


def archive_path_option(cardinality: jiig.Cardinality = None) -> jiig.Argument:
    return jiig.option('ARCHIVE_PATH',
                       ('-p', '--archive-path'),
                       jiig.adapters.existing_path,
                       description='Path to source archive file or folder',
                       cardinality=cardinality)


def date_max_option() -> jiig.Argument:
    return jiig.option('DATE_MAX',
                       '--date-max',
                       jiig.adapters.str_to_timestamp,
                       description='Maximum (latest) archive date')


def date_min_option() -> jiig.Argument:
    return jiig.option('DATE_MIN',
                       '--date-min',
                       jiig.adapters.str_to_timestamp,
                       description='Minimum (earliest) archive date')


def interval_max_option() -> jiig.Argument:
    return jiig.option('INTERVAL_MAX',
                       '--interval-max',
                       jiig.adapters.str_to_interval,
                       description='Maximum interval (n[HMS]) between saves to consider')


def interval_min_option() -> jiig.Argument:
    return jiig.option('INTERVAL_MIN',
                       '--interval-min',
                       jiig.adapters.str_to_interval,
                       description='Minimum interval (n[HMS]) between saves to consider')


def long_format_option() -> jiig.Argument:
    return jiig.bool_option('LONG_FORMAT',
                            ('-l', '--long'),
                            description='Long format to display extra information')


def method_option() -> jiig.Argument:
    return jiig.option('METHOD',
                       ('-m', '--method'),
                       description=f'Archive method',
                       default_value=DEFAULT_METHOD,
                       choices=get_method_names())


def no_confirmation_option() -> jiig.Argument:
    return jiig.bool_option('NO_CONFIRMATION',
                            '--no-confirmation',
                            description='Execute destructive actions without'
                                        ' prompting for confirmation')


def size_unit_binary_option() -> jiig.Argument:
    return jiig.bool_option('SIZE_UNIT_BINARY',
                            '--size-unit-binary',
                            description='Format size as binary 1024-based KiB, MiB, etc.')


def size_unit_decimal_option() -> jiig.Argument:
    return jiig.bool_option('SIZE_UNIT_DECIMAL',
                            '--size-unit-decimal',
                            description='Format size as decimal 1000-based KB, MB, etc.')


def source_folder_option(cardinality: jiig.Cardinality = None) -> jiig.Argument:
    return jiig.option('SOURCE_FOLDER',
                       ('-s', '--source-folder'),
                       jiig.adapters.folder_path,
                       description='Source folder',
                       default_value='.',
                       cardinality=cardinality)


def source_name_option() -> jiig.Argument:
    return jiig.option('SOURCE_NAME',
                       ('-n', '--name'),
                       description='Source name',
                       default_value=os.path.basename(os.getcwd()))


def tags_option() -> jiig.Argument:
    return jiig.option('TAGS',
                       ('-t', '--tags'),
                       description='Comma-separated archive tags')
