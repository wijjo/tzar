"""Archive support for rsync targets."""

from typing import Text, Iterator

from .base import ArchiveMethodBase
from tzar.archiver import archive_method


@archive_method('sync')
class ArchiveMethodSync(ArchiveMethodBase):
    def save(self,
             source_paths: Iterator[Text],
             target_path: Text,
             verbose: bool = False,
             progress: bool = False):
        pass
