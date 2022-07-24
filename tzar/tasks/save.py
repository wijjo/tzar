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
from tzar.runtime import TzarRuntime


@jiig.task(
    cli={
        'options': {
            'exclude': constants.OPTION_EXCLUDE,
            'progress': constants.OPTION_PROGRESS,
            'disable_timestamp': constants.OPTION_DISABLE_TIMESTAMP,
            'gitignore': constants.OPTION_GITIGNORE,
            'keep_list': constants.OPTION_KEEP_LIST,
            'pending': constants.OPTION_PENDING,
            'tags': constants.OPTION_TAGS,
            'archive_folder': constants.OPTION_ARCHIVE_FOLDER,
            'source_name': constants.OPTION_SOURCE_NAME,
            'source_folder': constants.OPTION_SOURCE_FOLDER,
            'method': constants.OPTION_METHOD,
        }
    }
)
def save(
    runtime: TzarRuntime,
    exclude: jiig.f.text(repeat=(None, None)),
    progress: jiig.f.boolean(),
    disable_timestamp: jiig.f.boolean(),
    gitignore: jiig.f.boolean(),
    keep_list: jiig.f.boolean(),
    pending: jiig.f.boolean(),
    tags: jiig.f.comma_list(),
    archive_folder: jiig.f.filesystem_folder(absolute_path=True) = constants.DEFAULT_ARCHIVE_FOLDER,
    source_name: jiig.f.text() = os.path.basename(os.getcwd()),
    source_folder: jiig.f.filesystem_folder(absolute_path=True) = '.',
    method: jiig.f.text(choices=TzarRuntime.get_method_names()) = constants.DEFAULT_METHOD,
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
    runtime.save_archive(source_folder,
                         archive_folder,
                         method,
                         source_name=source_name,
                         gitignore=gitignore,
                         excludes=exclude,
                         pending=pending,
                         timestamp=not disable_timestamp,
                         progress=progress,
                         keep_list=keep_list,
                         tags=tags)
