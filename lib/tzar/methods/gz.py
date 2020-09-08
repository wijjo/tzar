"""Support for GZ archives."""

from typing import List, Text

from tzar.archiver import archive_method

from .base import MethodData, ArchiveMethodBase
from .tarball import build_tarball_save_command


@archive_method('gz', file_extension='tar.gz', is_default=True)
class ArchiveMethodGZ(ArchiveMethodBase):
    def build_save_command(self, method_data: MethodData) -> List[Text]:
        return build_tarball_save_command(method_data, 'pigz', 'gzip')
