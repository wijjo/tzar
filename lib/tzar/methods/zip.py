"""Support for Zip archives."""

import os
from time import mktime
import zipfile
from typing import Text, Sequence, Optional

from tzar.archiver import archive_method

from .base import MethodSaveData, ArchiveMethodBase, MethodSaveResult, MethodListItem


@archive_method('zip')
class ArchiveMethodZip(ArchiveMethodBase):

    @classmethod
    def handle_get_name(cls, archive_name: Text) -> Text:
        """
        Required override to isolate base archive name and strip any extension as needed.

        :param archive_name: archive file name
        :return: stripped name suitable for further parsing
        """
        if archive_name.endswith('.zip'):
            return archive_name[:-4]
        return archive_name

    @classmethod
    def handle_save(cls, save_data: MethodSaveData) -> MethodSaveResult:
        """
        Required override for saving an archive.

        :param save_data: input parameters for save operation
        :return: save result data
        """
        cmd_args = ['zip', '-r', '-', '.', f'-i@{save_data.source_list_path}']
        if not save_data.verbose:
            cmd_args.append('-q')
        if save_data.pv_progress:
            cmd_args.extend(['|', 'pv', '-bret'])
        zip_path = save_data.archive_path + '.zip'
        cmd_args.extend(['>', zip_path])
        return MethodSaveResult(archive_path=zip_path, command_arguments=cmd_args)

    @classmethod
    def handle_list(cls, archive_path: Text) -> Sequence[MethodListItem]:
        """
        Required override for listing archive contents.

        :param archive_path: path of archive file or folder
        :return: sequence of archive items
        """
        with zipfile.ZipFile(archive_path, compression=zipfile.ZIP_DEFLATED) as zip_file:
            for info in zip_file.infolist():
                file_size = info.file_size if not info.is_dir() else None
                file_time = mktime(info.date_time + (0, 0, -1))
                yield MethodListItem(path=info.filename, time=file_time, size=file_size)

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
        if not archive_path.endswith('.zip'):
            return None
        return archive_path[:-4]
