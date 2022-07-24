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
Tzar prune command.

Pruning options provide flexibility for specifying different algorithms for
choosing which archives to purge.

Due to the destructive nature of these actions, an action summary is displayed,
followed by a confirmation prompt. A NO_CONFIRMATION option can disable the
confirmation prompt, e.g. for automation scripts.
"""

import os

import jiig

from tzar import constants
from tzar.runtime import TzarRuntime


# noinspection PyUnusedLocal
@jiig.task(
    cli={
        'options': {
            'age_min': constants.OPTION_AGE_MIN,
            'age_max': constants.OPTION_AGE_MAX,
            'date_min': constants.OPTION_DATE_MIN,
            'date_max': constants.OPTION_DATE_MAX,
            'interval_max': constants.OPTION_INTERVAL_MAX,
            'interval_min': constants.OPTION_INTERVAL_MIN,
            'tags': constants.OPTION_TAGS,
            'no_confirmation': constants.OPTION_NO_CONFIRMATION,
            'archive_folder': constants.OPTION_ARCHIVE_FOLDER,
            'source_name': constants.OPTION_SOURCE_NAME,
            'source_folder': constants.OPTION_SOURCE_FOLDER,
        }
    }
)
def prune(
    runtime: TzarRuntime,
    age_max: jiig.f.age(),
    age_min: jiig.f.age(),
    date_max: jiig.f.timestamp(),
    date_min: jiig.f.timestamp(),
    interval_max: jiig.f.interval(),
    interval_min: jiig.f.interval(),
    tags: jiig.f.comma_list(),
    no_confirmation: jiig.f.boolean(),
    archive_folder: jiig.f.filesystem_folder(absolute_path=True) = constants.DEFAULT_ARCHIVE_FOLDER,
    source_name: jiig.f.text() = os.path.basename(os.getcwd()),
    source_folder: jiig.f.filesystem_folder(absolute_path=True) = '.',
):
    """
    Prune archives to save space. [^destructive]

    :param runtime: Jiig runtime API.
    :param age_max: Maximum archive age [^age_option].
    :param age_min: Minimum archive age [^age_option].
    :param date_max: Maximum (latest) archive date.
    :param date_min: Minimum (earliest) archive date.
    :param interval_max: Maximum interval (n[HMS]) between saves to consider.
    :param interval_min: Minimum interval (n[HMS]) between saves to consider.
    :param tags: Comma-separated archive tags.
    :param no_confirmation: Execute destructive actions without prompting for confirmation.
    :param archive_folder: Archive folder.
    :param source_name: Source name.
    :param source_folder: Source folder.
    """
    for item in runtime.list_catalog(
            source_folder,
            archive_folder,
            source_name=source_name,
            date_min=date_min,
            date_max=date_max,
            age_min=age_min,
            age_max=age_max,
            interval_min=interval_min,
            interval_max=interval_max,
            tags=tags):
        print(f'--> {item.time_string}')
