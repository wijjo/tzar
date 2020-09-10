"""Support for GZ archives."""

from tzar.archiver import archive_method

from .base import MethodData, ArchiveMethodBase, MethodSaveData
from .tarball import handle_tarball_save


@archive_method('gz', is_default=True)
class ArchiveMethodGZ(ArchiveMethodBase):
    def handle_save(self, method_data: MethodData) -> MethodSaveData:
        return handle_tarball_save(method_data, compressors=['pigz', 'gzip'], extension='gz')
