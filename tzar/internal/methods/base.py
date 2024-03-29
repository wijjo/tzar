# Copyright (C) 2021-2023, Steven Cooper
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

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from jiig.util.filesystem import find_system_program
from jiig.util.log import log_warning

PV_INSTALLED = bool(find_system_program('pv'))
PV_WARNED = False


@dataclass
class MethodSaveData:
    """Input data for archive saving."""

    source_path: Path
    source_list_path: Path
    archive_path: Path
    verbose: bool
    dry_run: bool
    progress: bool
    total_bytes: int
    total_files: int
    total_folders: int

    @property
    def pv_progress(self) -> bool:
        """
        Use instead of `progress` member when "pv" is required.

        :return: True if progress is required and pv is available
        """
        if not self.progress:
            return False
        if not PV_INSTALLED:
            global PV_WARNED
            if not PV_WARNED:
                log_warning('Please install the "pv" program in order'
                            ' to use the progress option.')
                PV_WARNED = True
            return False
        return True


@dataclass
class MethodSaveResult:
    """Output data received after saving archive."""
    archive_path: Path
    command_arguments: list[str]


@dataclass
class MethodListItem:
    """Data received for an archive file when listing archive contents."""
    path: Path
    time: float
    # File size or None if it is a folder.
    size: int | None


class ArchiveMethodBase:
    """Base archive method class."""

    @classmethod
    def handle_get_name(cls,
                        archive_name: str,
                        ) -> str:
        """
        Required override to isolate base archive name and strip any extension as needed.

        :param archive_name: archive file name
        :return: stripped name suitable for further parsing
        """
        raise NotImplementedError

    @classmethod
    def handle_save(cls,
                    save_data: MethodSaveData,
                    ) -> MethodSaveResult:
        """
        Required override for saving an archive.

        :param save_data: input parameters for save operation
        :return: save result data
        """
        raise NotImplementedError

    @classmethod
    def handle_list(cls,
                    archive_path: Path,
                    ) -> Sequence[MethodListItem]:
        """
        Required override for listing archive contents.

        Returned sequence may be unsorted, since it will be sorted later.

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
        raise NotImplementedError
