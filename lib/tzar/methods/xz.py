"""Support for XZ archives."""

import os
from typing import Text, Sequence, Optional

from tzar.archiver import archive_method

from .base import MethodSaveData, ArchiveMethodBase, MethodSaveResult, MethodListItem
from .tarball import handle_tarball_save, handle_tarball_list


@archive_method('xz')
class ArchiveMethodXZ(ArchiveMethodBase):

    @classmethod
    def handle_save(cls, save_data: MethodSaveData) -> MethodSaveResult:
        """
        Required override for saving an archive.

        :param save_data: input parameters for save operation
        :return: save result data
        """
        return handle_tarball_save(save_data, compressors=['pixz', 'xz'], extension='xz')

    @classmethod
    def handle_list(cls, archive_path: Text) -> Sequence[MethodListItem]:
        """
        Required override for listing archive contents.

        :param archive_path: path of archive file or folder
        :return: sequence of item data objects, one per archived file
        """
        return handle_tarball_list(archive_path, compression='xz')

    @classmethod
    def check_supported(cls, archive_path: Text) -> Optional[Text]:
        """
        Required override for testing if an archive is handled by this method.

        :param archive_path: path of archive file or folder
        :return: base filename or path if it is handled or None if it is not
        """
        if os.path.isfile(archive_path) and archive_path.endswith('.tar.xz'):
            return archive_path[:-7]
        return None
