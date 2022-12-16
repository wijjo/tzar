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
Tarball archive general support.
"""

import tarfile
from pathlib import Path
from typing import Sequence

from jiig.util.filesystem import choose_program_alternative
from jiig.util.collections import make_list

from tzar.archive_method import MethodSaveData, MethodSaveResult, MethodListItem


def handle_tarball_save(save_data: MethodSaveData,
                        compressors: list[str] | str = None,
                        extension: str = None,
                        ) -> MethodSaveResult:
    """
    Build command arguments for saving tarball with optional compression+progress.

    :param save_data: specification data for saving tarball archive
    :param extension: optional extension without leading '.' appended to ".tar"
    :param compressors: compression programs, with optional arguments when it's a sequence
    :return:
    """
    cmd_args = ['tar', f'cf', '-', '-T', str(save_data.source_list_path)]
    if save_data.verbose:
        cmd_args.append('-v')
    # choose_program_alternative() returns a command argument list.
    if compressors:
        compression_program = choose_program_alternative(
            *make_list(compressors, strings=True),
            required=True)
        cmd_args.extend(['|'] + compression_program)
    if save_data.pv_progress:
        # Create a pipeline with "pv" for progress reporting.
        cmd_args.extend(['|', 'pv', '-bret'])
    archive_path_parts = [str(save_data.archive_path), 'tar']
    if extension:
        archive_path_parts.append(extension)
    archive_path = '.'.join(archive_path_parts)
    cmd_args.extend(['>', archive_path])
    return MethodSaveResult(archive_path=Path(archive_path), command_arguments=cmd_args)


def handle_tarball_list(archive_path: Path,
                        compression: str = None
                        ) -> Sequence[MethodListItem]:
    """
    Implementation to list tarball contents.

    :param archive_path: archive tarball file path
    :param compression: optional compression specification, e.g. 'gz'
    :return: sequence of archive items
    """
    mode = f'r:{compression}' if compression else 'r'
    with tarfile.open(archive_path, mode=mode) as tar_file:
        for info in tar_file.getmembers():
            file_size = info.size if not info.isdir() else None
            yield MethodListItem(path=Path(info.name), time=info.mtime, size=file_size)


def handle_tarball_get_name(archive_name: str,
                            extension: str = None,
                            ) -> str:
    """
    Implementation to preprocess archive name for further parsing.

    :param archive_name: archive file name
    :param extension: optional extension without leading '.' appended to ".tar"
    :return: stripped name suitable for further parsing
    """
    full_extension = f'.tar.{extension}'
    if archive_name.endswith(full_extension):
        return archive_name[:-len(full_extension)]
    return archive_name
