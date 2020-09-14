DEFAULT_ARCHIVE_FOLDER = '../tzarchive'
TARGET_TIMESTAMP = '%Y%m%d-%H%M%S'
ARCHIVE_NAME_PATTERN = r'^' \
                       r'(?P<name>{name})_' \
                       r'(?:' \
                           r'(?P<year>\d\d\d\d)' \
                           r'(?P<month>\d\d)' \
                           r'(?P<day>\d\d)' \
                           r'-' \
                           r'(?P<hours>\d\d)' \
                           r'(?P<minutes>\d\d)' \
                           r'(?P<seconds>\d\d)' \
                       r')?' \
                       r'(?:_' \
                           r'(?P<comment>.+)' \
                       r')?' \
                       r'$'
