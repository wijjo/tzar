"""Support for Zip archives."""

from typing import Text, Iterator

from .base import ArchiveMethodBase
from tzar.archiver import archive_method


@archive_method('zip')
class ArchiveMethodZip(ArchiveMethodBase):
    def save(self, source_paths: Iterator[Text], target_path: Text):
        pass
