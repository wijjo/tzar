import re

DEFAULT_ARCHIVE_FOLDER = '../tzarchive'
TIMESTAMP_FORMAT = '%Y%m%d-%H%M%S'
TIMESTAMP_REGEX = re.compile(r'(?P<year>\d\d\d\d)'
                             r'(?P<month>\d\d)'
                             r'(?P<day>\d\d)'
                             r'-'
                             r'(?P<hours>\d\d)'
                             r'(?P<minutes>\d\d)'
                             r'(?P<seconds>\d\d)')
