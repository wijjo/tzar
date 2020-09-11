"""Support for Zip archives."""

import os
from time import mktime
import zipfile
from typing import Text, Sequence

from tzar.archiver import archive_method

from .base import MethodSaveData, ArchiveMethodBase, MethodSaveResult, MethodListItem


@archive_method('zip')
class ArchiveMethodZip(ArchiveMethodBase):

    def handle_save(self, save_data: MethodSaveData) -> MethodSaveResult:
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
        zip_path = save_data.target_path + '.zip'
        cmd_args.extend(['>', zip_path])
        return MethodSaveResult(target_path=zip_path, command_arguments=cmd_args)

    def handle_list(self, archive_path: Text) -> Sequence[MethodListItem]:
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
    def is_supported_archive(cls, archive_path: Text) -> bool:
        """
        Required override for testing if an archive is handled by this method.

        :param archive_path: path of archive file or folder
        :return: True if the archive type is handled by the archive method object
        """
        return os.path.isfile(archive_path) and archive_path.endswith('.zip')
