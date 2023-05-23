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

"""Tzar compare command."""

import jiig


@jiig.task
def compare(
    _runtime: jiig.Runtime,
    _archive_path: jiig.f.filesystem_object(exists=True),
    _source_folder: jiig.f.filesystem_folder(absolute_path=True) = '.',
):
    """
    Compare archive to existing files.

    :param _runtime: Jiig runtime API.
    :param _archive_path: Path to source archive file or folder.
    :param _source_folder: Source folder.
    """
    raise NotImplementedError
