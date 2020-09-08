"""Support for XZ archives."""

from typing import List, Text

from tzar.archiver import archive_method

from .base import MethodData, ArchiveMethodBase
from .tarball import build_tarball_save_command


@archive_method('xz', file_extension='tar.xz')
class ArchiveMethodXZ(ArchiveMethodBase):
    def build_save_command(self, method_data: MethodData) -> List[Text]:
        return build_tarball_save_command(method_data, 'pixz', 'xz')
