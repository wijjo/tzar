"""Support for XZ archives."""

import os
from typing import Text, Sequence, Optional

from .base import MethodSaveData, ArchiveMethodBase, MethodSaveResult, MethodListItem
from .tarball import handle_tarball_save, handle_tarball_list, handle_tarball_get_name


class ArchiveMethodXZ(ArchiveMethodBase):

    @classmethod
    def handle_get_name(cls, archive_name: Text) -> Text:
        """
        Required override to isolate base archive name and strip any extension as needed.

        :param archive_name: archive file name
        :return: stripped name suitable for further parsing
        """
        return handle_tarball_get_name(archive_name, extension='xz')

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
    def check_supported(cls,
                        archive_path: Text,
                        assumed_type: int = None,
                        ) -> Optional[Text]:
        """
        Required override for testing if an archive is handled by a particular method.

        :param archive_path: path of archive file or folder
        :param assumed_type: For testing, 1=file, 2=folder, None=check physical object
        :return: base filename or path if it is handled or None if it is not
        """
        if assumed_type is None:
            if not os.path.isfile(archive_path):
                return None
        elif assumed_type != 1:
            return None
        if not archive_path.endswith('.tar.xz'):
            return None
        return archive_path[:-7]
