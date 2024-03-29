# Copyright (C) 2021-2022, Steven Cooper
#
# This file is part of Tzar.
#
# Tzar is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Tzar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Tzar.  If not, see <https://www.gnu.org/licenses/>.

"""
Archive support for file-based cloning using rsync.
"""

from pathlib import Path
from typing import Sequence

from jiig.util.filesystem import create_folder

from .base import (
    ArchiveMethodBase,
    MethodListItem,
    MethodSaveData,
    MethodSaveResult,
)


class ArchiveMethodSync(ArchiveMethodBase):

    @classmethod
    def handle_get_name(cls,
                        archive_name: str,
                        ) -> str:
        """
        Required override to isolate base archive name and strip any extension as needed.

        :param archive_name: archive file name
        :return: stripped name suitable for further parsing
        """
        return archive_name

    @classmethod
    def handle_save(cls,
                    save_data: MethodSaveData,
                    ) -> MethodSaveResult:
        """
        Required override for saving an archive.

        :param save_data: input parameters for save operation
        :return: save result data
        """
        create_folder(save_data.archive_path.parent)
        cmd_args = ['rsync', '-a', f'--include-from={save_data.source_list_path}']
        if save_data.verbose:
            cmd_args.append('-v')
        cmd_args.extend([f'{save_data.source_path}/', f'{save_data.archive_path}/'])
        return MethodSaveResult(archive_path=save_data.archive_path, command_arguments=cmd_args)

    @classmethod
    def handle_list(cls,
                    archive_path: Path,
                    ) -> Sequence[MethodListItem]:
        """
        Required override for listing archive contents.

        :param archive_path: path of archive file or folder
        :return: sequence of item data objects, one per archived file
        """
        raise NotImplementedError

    @classmethod
    def check_supported(cls,
                        archive_path: Path,
                        assumed_type: int = None,
                        ) -> Path | None:
        """
        Required override for testing if an archive is handled by a particular method.

        :param archive_path: path of archive file or folder
        :param assumed_type: For testing, 1=file, 2=folder, None=check physical object
        :return: base filename or path if it is handled or None if it is not
        """
        if assumed_type == 2 or (assumed_type is None and archive_path.is_dir()):
            return archive_path
        return None
