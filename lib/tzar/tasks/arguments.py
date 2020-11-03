from jiig import Arg
from jiig.arg import Boolean, DateTime, File, Folder, Integer, Interval, String
from jiig.arg.argument_type import Cardinality

from tzar.internal.archiver import get_method_names, DEFAULT_METHOD
from tzar.internal.constants import DEFAULT_ARCHIVE_FOLDER


class AgeMaxArg(Arg):
    def __init__(self, positional: bool = False):
        super().__init__('AGE_MAX',
                         Integer,
                         description='Maximum archive age [age_option]',
                         flags='--age-max',
                         positional=positional),


class AgeMinArg(Arg):
    def __init__(self, positional: bool = False):
        super().__init__('AGE_MIN',
                         Integer,
                         description='Minimum archive age [age_option]',
                         flags='--age-min',
                         positional=positional),


class ArchiveFolderArg(Arg):
    def __init__(self, positional: bool = False):
        super().__init__('ARCHIVE_FOLDER',
                         Folder(must_exist=True),
                         description=f'Archive folder',
                         default_value=DEFAULT_ARCHIVE_FOLDER,
                         flags=['-f', '--archive-folder'],
                         positional=positional),


class ArchivePathArg(Arg):
    def __init__(self, positional: bool = False, cardinality: Cardinality = None):
        super().__init__('ARCHIVE_PATH',
                         File(must_exist=True, allow_folder=True),
                         description='Path to source archive file or folder',
                         flags=['-p', '--archive-path'],
                         cardinality=cardinality,
                         positional=positional),


class DateMaxArg(Arg):
    def __init__(self, positional: bool = False):
        super().__init__('DATE_MAX',
                         DateTime,
                         description='Maximum (latest) archive date',
                         flags='--date-max',
                         positional=positional),


class DateMinArg(Arg):
    def __init__(self, positional: bool = False):
        super().__init__('DATE_MIN',
                         DateTime,
                         description='Minimum (earliest) archive date',
                         flags='--date-min',
                         positional=positional),


class IntervalMaxArg(Arg):
    def __init__(self, positional: bool = False):
        super().__init__('INTERVAL_MAX',
                         Interval,
                         description='Maximum interval (n[HMS]) between saves to consider',
                         flags='--interval-max',
                         positional=positional),


class IntervalMinArg(Arg):
    def __init__(self, positional: bool = False):
        super().__init__('INTERVAL_MIN',
                         Interval,
                         description='Minimum interval (n[HMS]) between saves to consider',
                         flags='--interval-min',
                         positional=positional),


class LongFormatArg(Arg):
    def __init__(self, positional: bool = False):
        super().__init__('LONG_FORMAT',
                         Boolean,
                         description='Long format to display extra information',
                         flags=['-l', '--long'],
                         positional=positional),


class MethodArg(Arg):
    def __init__(self, positional: bool = False):
        super().__init__('METHOD',
                         String(choices=get_method_names()),
                         description=f'Archive method',
                         default_value=DEFAULT_METHOD,
                         flags=['-m', '--method'],
                         positional=positional),


class NoConfirmationArg(Arg):
    def __init__(self, positional: bool = False):
        super().__init__('NO_CONFIRMATION',
                         Boolean,
                         description='Execute destructive actions without'
                                     ' prompting for confirmation',
                         flags='--no-confirmation',
                         positional=positional),


class SizeUnitBinaryArg(Arg):
    def __init__(self, positional: bool = False):
        super().__init__('SIZE_UNIT_BINARY',
                         Boolean,
                         description='Format size as binary 1024-based KiB, MiB, etc.',
                         flags='--size-unit-binary',
                         positional=positional),


class SizeUnitDecimalArg(Arg):
    def __init__(self, positional: bool = False):
        super().__init__('SIZE_UNIT_DECIMAL',
                         Boolean,
                         description='Format size as decimal 1000-based KB, MB, etc.',
                         flags='--size-unit-decimal',
                         positional=positional),


class SourceFolderArg(Arg):
    def __init__(self, positional: bool = False, cardinality: Cardinality = None):
        super().__init__('SOURCE_FOLDER',
                         Folder(must_exist=True),
                         description='Source folder',
                         default_value='.',
                         flags=['-s', '--source-folder'],
                         cardinality=cardinality,
                         positional=positional),


class SourceNameArg(Arg):
    def __init__(self, positional: bool = False):
        super().__init__('SOURCE_NAME',
                         String,
                         description='Source name (default: <working folder name>)',
                         flags=['-n', '--name'],
                         positional=positional),


class TagsArg(Arg):
    def __init__(self, positional: bool = False):
        super().__init__('TAGS',
                         String,
                         description='Comma-separated archive tags',
                         flags=['-t', '--tags'],
                         positional=positional),
