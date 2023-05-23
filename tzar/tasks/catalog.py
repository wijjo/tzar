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

"""Tzar catalog command."""

import os

import jiig

from tzar.internal import (
    format_catalog_table,
    get_catalog_spec,
    list_catalog,
)


@jiig.task
def catalog(
    runtime: jiig.Runtime,
    age_max: jiig.f.age(),
    age_min: jiig.f.age(),
    date_max: jiig.f.timestamp(),
    date_min: jiig.f.timestamp(),
    interval_max: jiig.f.interval(),
    interval_min: jiig.f.interval(),
    tags: jiig.f.comma_list(),
    unit_format: jiig.f.text(choices=('b', 'd')) = 'b',
    archive_folder: jiig.f.filesystem_folder(absolute_path=True) = None,
    source_name: jiig.f.text() = os.path.basename(os.getcwd()),
    source_folder: jiig.f.filesystem_folder(absolute_path=True) = '.',
):
    """
    List archive catalog folder.

    :param runtime: Jiig runtime API.
    :param age_max: Maximum archive age [^age_option].
    :param age_min: Minimum archive age [^age_option].
    :param date_max: Maximum (latest) archive date.
    :param date_min: Minimum (earliest) archive date.
    :param interval_max: Maximum interval (n[HMS]) between saves to consider.
    :param interval_min: Minimum interval (n[HMS]) between saves to consider.
    :param tags: Comma-separated archive tags.
    :param unit_format: 'b' for KiB/MiB/... or 'd' for KB/MB/... (default: 'b')
    :param archive_folder: Archive folder.
    :param source_name: Source name.
    :param source_folder: Source folder.
    """
    # Get full catalog spec based on user-provided one or default folder hierarchy.
    catalog_spec = get_catalog_spec(runtime, source_folder, archive_folder, source_name)
    with runtime.context(source_name=catalog_spec.source_name,
                         archive_folder=catalog_spec.archive_folder,
                         ) as context:
        context.heading(1, '{source_name} archive catalog from "{archive_folder}"')
        for line in format_catalog_table(
            list_catalog(
                runtime,
                catalog_spec,
                date_min=date_min,
                date_max=date_max,
                age_min=age_min,
                age_max=age_max,
                interval_min=interval_min,
                interval_max=interval_max,
                tags=tags,
            ),
            unit_format=unit_format,
        ):
            print(line)
