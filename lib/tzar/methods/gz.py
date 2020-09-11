"""Support for GZ archives."""

import os
from typing import Text, Sequence

from tzar.archiver import archive_method

from .base import MethodSaveData, ArchiveMethodBase, MethodSaveResult, MethodListItem
from .tarball import handle_tarball_save, handle_tarball_list


@archive_method('gz', is_default=True)
class ArchiveMethodGZ(ArchiveMethodBase):

    def handle_save(self, save_data: MethodSaveData) -> MethodSaveResult:
        """
        Required override for saving an archive.

        :param save_data: input parameters for save operation
        :return: save result data
        """
        return handle_tarball_save(save_data, compressors=['pigz', 'gzip'], extension='gz')

    def handle_list(self, archive_path: Text) -> Sequence[MethodListItem]:
        """
        Required override for listing archive contents.

        :param archive_path: path of archive file or folder
        :return: sequence of item data objects, one per archived file
        """
        return handle_tarball_list(archive_path, compression='gz')

    @classmethod
    def is_supported_archive(cls, archive_path: Text) -> bool:
        """
        Required override for testing if an archive is handled by this method.

        :param archive_path: path of archive file or folder
        :return: True if the archive type is handled by the archive method object
        """
        return os.path.isfile(archive_path) and archive_path.endswith('.tar.gz')
