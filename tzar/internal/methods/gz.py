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
Support for GZ archives.
"""

from pathlib import Path
from typing import Sequence

from .base import (
    ArchiveMethodBase,
    MethodListItem,
    MethodSaveData,
    MethodSaveResult,
)

from .tarball import handle_tarball_save, handle_tarball_list, handle_tarball_get_name


class ArchiveMethodGZ(ArchiveMethodBase):

    @classmethod
    def handle_get_name(cls,
                        archive_name: str,
                        ) -> str:
        """
        Required override to isolate base archive name and strip any extension as needed.

        :param archive_name: archive file name
        :return: stripped name suitable for further parsing
        """
        return handle_tarball_get_name(archive_name, extension='gz')

    @classmethod
    def handle_save(cls,
                    save_data: MethodSaveData,
                    ) -> MethodSaveResult:
        """
        Required override for saving an archive.

        :param save_data: input parameters for save operation
        :return: save result data
        """
        return handle_tarball_save(save_data, compressors=['pigz', 'gzip'], extension='gz')

    @classmethod
    def handle_list(cls,
                    archive_path: Path,
                    ) -> Sequence[MethodListItem]:
        """
        Required override for listing archive contents.

        :param archive_path: path of archive file or folder
        :return: sequence of item data objects, one per archived file
        """
        return handle_tarball_list(archive_path, compression='gz')

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
        if assumed_type is None:
            if not archive_path.is_file():
                return None
        elif assumed_type != 1:
            return None
        if not str(archive_path).endswith('.tar.gz'):
            return None
        return Path(str(archive_path)[:-7])
