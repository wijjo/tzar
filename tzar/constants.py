import re

DEFAULT_METHOD = 'gz'
DEFAULT_ARCHIVE_FOLDER = '../tzarchive'
TIMESTAMP_FORMAT = '%Y%m%d-%H%M%S'
TIMESTAMP_REGEX = re.compile(r'(?P<year>\d\d\d\d)'
                             r'(?P<month>\d\d)'
                             r'(?P<day>\d\d)'
                             r'-'
                             r'(?P<hours>\d\d)'
                             r'(?P<minutes>\d\d)'
                             r'(?P<seconds>\d\d)')

# Option flags, defined as constants for uniformity.
OPTION_ARCHIVE_FOLDER = ('-f', '--archive-folder')
OPTION_SOURCE_NAME = ('-n', '--name')
OPTION_SOURCE_FOLDER = ('-s', '--source-folder')
OPTION_METHOD = ('-m', '--method')
OPTION_TAGS = ('-t', '--tags')
OPTION_SIZE_UNIT_BINARY = '--size-unit-binary'
OPTION_SIZE_UNIT_DECIMAL = '--size-unit-decimal'
OPTION_LONG_FORMAT = ('-l', '--long')
OPTION_AGE_MAX = '--age-max'
OPTION_AGE_MIN = '--age-min'
OPTION_DATE_MAX = '--date-max'
OPTION_DATE_MIN = '--date-min'
OPTION_INTERVAL_MAX = '--interval-max'
OPTION_INTERVAL_MIN = '--interval-min'
OPTION_NO_CONFIRMATION = '--no-confirmation'
OPTION_EXCLUDE = ('-e', '--exclude')
OPTION_PROGRESS = ('-p', '--progress')
OPTION_DISABLE_TIMESTAMP = ('-T', '--no-timestamp')
OPTION_GITIGNORE = '--gitignore'
OPTION_KEEP_LIST = '--keep-list'
OPTION_PENDING = '--pending'
