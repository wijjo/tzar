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

"""Tzar save command."""

import os

import jiig

from tzar import constants
from tzar.internal import (
    METHOD_NAMES,
    get_catalog_spec,
    save_archive,
)


# noinspection PyUnusedLocal
@jiig.task
def save(
    runtime: jiig.Runtime,
    exclude: jiig.f.text(repeat=()),
    progress: jiig.f.boolean(),
    disable_timestamp: jiig.f.boolean(),
    gitignore: jiig.f.boolean(),
    keep_list: jiig.f.boolean(),
    pending: jiig.f.boolean(),
    tags: jiig.f.comma_list(),
    archive_folder: jiig.f.filesystem_folder(absolute_path=True) = None,
    source_name: jiig.f.text() = None,
    source_folder: jiig.f.filesystem_folder(absolute_path=True) = None,
    method: jiig.f.text(choices=METHOD_NAMES) = constants.DEFAULT_METHOD,
):
    """
    Save an archive of the working folder or another folder.

    :param runtime: Jiig runtime API.
    :param exclude: Exclusion pattern(s), including gitignore-style wildcards.
    :param progress: Display progress statistics.
    :param disable_timestamp: Disable adding timestamp to name.
    :param gitignore: Use .gitignore exclusions.
    :param keep_list: Do not delete temporary file list when done.
    :param pending: Save only modified version-controlled files.
    :param tags: Comma-separated archive tags.
    :param archive_folder: Archive folder.
    :param source_name: Source name.
    :param source_folder: Source folder.
    :param method: Archive method.
    """
    save_archive(get_catalog_spec(source_folder, archive_folder, source_name),
                 method,
                 gitignore=gitignore,
                 excludes=exclude,
                 pending=pending,
                 timestamp=not disable_timestamp,
                 progress=progress,
                 keep_list=keep_list,
                 tags=tags)
