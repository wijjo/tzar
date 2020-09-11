"""Archive support for file-based cloning using rsync."""

import os
from typing import Text, Sequence

from jiig.utility.filesystem import create_folder
from tzar.archiver import archive_method

from .base import MethodSaveData, ArchiveMethodBase, MethodSaveResult, MethodListItem


@archive_method('files')
class ArchiveMethodSync(ArchiveMethodBase):

    def handle_save(self, save_data: MethodSaveData) -> MethodSaveResult:
        """
        Required override for saving an archive.

        :param save_data: input parameters for save operation
        :return: save result data
        """
        create_folder(os.path.dirname(save_data.target_path))
        cmd_args = ['rsync', '-a', f'--include-from={save_data.source_list_path}']
        if save_data.verbose:
            cmd_args.append('-v')
        cmd_args.extend([f'{save_data.source_path}/', f'{save_data.target_path}/'])
        return MethodSaveResult(target_path=save_data.target_path, command_arguments=cmd_args)

    def handle_list(self, archive_path: Text) -> Sequence[MethodListItem]:
        """
        Required override for listing archive contents.

        :param archive_path: path of archive file or folder
        :return: sequence of item data objects, one per archived file
        """
        raise NotImplementedError

    @classmethod
    def is_supported_archive(cls, archive_path: Text) -> bool:
        """
        Required override for testing if an archive is handled by this method.

        :param archive_path: path of archive file or folder
        :return: True if the archive type is handled by the archive method object
        """
        return os.path.isdir(archive_path)
