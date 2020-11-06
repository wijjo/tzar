import os

from jiig import arg, argument, Argument, Cardinality

from tzar.internal.archiver import get_method_names, DEFAULT_METHOD
from tzar.internal.constants import DEFAULT_ARCHIVE_FOLDER


def age_max_argument() -> Argument:
    return argument('AGE_MAX',
                    arg.integer,
                    description='Maximum archive age [age_option]',
                    flags='--age-max')


def age_min_argument() -> Argument:
    return argument('AGE_MIN',
                    arg.integer,
                    description='Minimum archive age [age_option]',
                    flags='--age-min')


def archive_folder_argument() -> Argument:
    return argument('ARCHIVE_FOLDER',
                    arg.folder_path(must_exist=True),
                    description='Archive folder',
                    default_value=DEFAULT_ARCHIVE_FOLDER,
                    flags=['-f', '--archive-folder'])


def archive_path_argument(positional: bool = False, cardinality: Cardinality = None) -> Argument:
    return argument('ARCHIVE_PATH',
                    arg.file_path(must_exist=True, allow_folder=True),
                    description='Path to source archive file or folder',
                    flags=['-p', '--archive-path'],
                    cardinality=cardinality,
                    positional=positional)


def date_max_argument() -> Argument:
    return argument('DATE_MAX',
                    arg.date_time,
                    description='Maximum (latest) archive date',
                    flags='--date-max')


def date_min_argument() -> Argument:
    return argument('DATE_MIN',
                    arg.date_time,
                    description='Minimum (earliest) archive date',
                    flags='--date-min')


def interval_max_argument() -> Argument:
    return argument('INTERVAL_MAX',
                    arg.interval,
                    description='Maximum interval (n[HMS]) between saves to consider',
                    flags='--interval-max')


def interval_min_argument() -> Argument:
    return argument('INTERVAL_MIN',
                    arg.interval,
                    description='Minimum interval (n[HMS]) between saves to consider',
                    flags='--interval-min')


def long_format_argument() -> Argument:
    return argument('LONG_FORMAT',
                    arg.boolean,
                    description='Long format to display extra information',
                    flags=['-l', '--long'])


def method_argument() -> Argument:
    return argument('METHOD',
                    arg.text,
                    description=f'Archive method',
                    default_value=DEFAULT_METHOD,
                    choices=get_method_names(),
                    flags=['-m', '--method'])


def no_confirmation_argument() -> Argument:
    return argument('NO_CONFIRMATION',
                    arg.boolean,
                    description='Execute destructive actions without'
                                ' prompting for confirmation',
                    flags='--no-confirmation')


def size_unit_binary_argument() -> Argument:
    return argument('SIZE_UNIT_BINARY',
                    arg.boolean,
                    description='Format size as binary 1024-based KiB, MiB, etc.',
                    flags='--size-unit-binary')


def size_unit_decimal_argument() -> Argument:
    return argument('SIZE_UNIT_DECIMAL',
                    arg.boolean,
                    description='Format size as decimal 1000-based KB, MB, etc.',
                    flags='--size-unit-decimal')


def source_folder_argument(cardinality: Cardinality = None) -> Argument:
    return argument('SOURCE_FOLDER',
                    arg.folder_path(must_exist=True),
                    description='Source folder',
                    default_value='.',
                    flags=['-s', '--source-folder'],
                    cardinality=cardinality)


def source_name_argument() -> Argument:
    return argument('SOURCE_NAME',
                    arg.text,
                    description='Source name',
                    default_value=os.path.basename(os.getcwd()),
                    flags=['-n', '--name'])


def tags_argument() -> Argument:
    return argument('TAGS',
                    arg.text,
                    description='Comma-separated archive tags',
                    flags=['-t', '--tags'])
