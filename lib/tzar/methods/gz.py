"""Support for GZ archives."""

from typing import Text, Iterator

from .base import ArchiveMethodBase
from tzar.archiver import archive_method


@archive_method('gz', is_default=True)
class ArchiveMethodGZ(ArchiveMethodBase):
    def save(self, source_paths: Iterator[Text], target_path: Text):
        full_target_path = target_path + '.tar.gz'
        for source_path in source_paths:
            print(f'GZ: {source_path} -> {full_target_path}')
