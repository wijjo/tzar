"""Archive support for file-based cloning using rsync."""

import os
from typing import Text, Sequence, Optional

from jiig.utility.filesystem import create_folder
from tzar.internal.archiver import archive_method

from .base import MethodSaveData, ArchiveMethodBase, MethodSaveResult, MethodListItem


@archive_method('files')
class ArchiveMethodSync(ArchiveMethodBase):

    @classmethod
    def handle_get_name(cls, archive_name: Text) -> Text:
        """
        Required override to isolate base archive name and strip any extension as needed.

        :param archive_name: archive file name
        :return: stripped name suitable for further parsing
        """
        return archive_name

    @classmethod
    def handle_save(cls, save_data: MethodSaveData) -> MethodSaveResult:
        """
        Required override for saving an archive.

        :param save_data: input parameters for save operation
        :return: save result data
        """
        create_folder(os.path.dirname(save_data.archive_path))
        cmd_args = ['rsync', '-a', f'--include-from={save_data.source_list_path}']
        if save_data.verbose:
            cmd_args.append('-v')
        cmd_args.extend([f'{save_data.source_path}/', f'{save_data.archive_path}/'])
        return MethodSaveResult(archive_path=save_data.archive_path, command_arguments=cmd_args)

    @classmethod
    def handle_list(cls, archive_path: Text) -> Sequence[MethodListItem]:
        """
        Required override for listing archive contents.

        :param archive_path: path of archive file or folder
        :return: sequence of item data objects, one per archived file
        """
        raise NotImplementedError

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
        if assumed_type == 2 or (assumed_type is None and os.path.isdir(archive_path)):
            return archive_path
        return None
