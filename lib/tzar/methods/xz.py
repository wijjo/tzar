"""Support for XZ archives."""

from typing import Text, Iterator

from .base import ArchiveMethodBase
from tzar.archiver import archive_method


@archive_method('xz')
class ArchiveMethodXZ(ArchiveMethodBase):
    def save(self, source_paths: Iterator[Text], target_path: Text):
        pass
