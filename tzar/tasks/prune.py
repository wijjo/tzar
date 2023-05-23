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

import jiig
from jiig.util.filesystem import delete_file, delete_folder

from tzar.internal import (
    format_catalog_table,
    get_catalog_spec,
    list_catalog,
)


@jiig.task
def prune(
    runtime: jiig.Runtime,
    age_max: jiig.f.age(),
    age_min: jiig.f.age(),
    date_max: jiig.f.timestamp(),
    date_min: jiig.f.timestamp(),
    interval_max: jiig.f.interval(),
    interval_min: jiig.f.interval(),
    tags: jiig.f.comma_list(),
    no_confirmation: jiig.f.boolean(),
    archive_folder: jiig.f.filesystem_folder(absolute_path=True),
    source_name: jiig.f.text(),
    source_folder: jiig.f.filesystem_folder(absolute_path=True),
):
    """
    Prune archives to save space. [^destructive]

    :param runtime: Jiig runtime API.
    :param age_max: Maximum archive age [^age_option].
    :param age_min: Minimum archive age [^age_option].
    :param date_max: Maximum (latest) archive date.
    :param date_min: Minimum (earliest) archive date.
    :param interval_max: Maximum interval (n[HMS]) between saves to consider.
    :param interval_min: Minimum interval (n[HMS]) between saves to consider (default: 1H).
    :param tags: Comma-separated archive tags.
    :param no_confirmation: Execute destructive actions without prompting for confirmation.
    :param archive_folder: Archive folder.
    :param source_name: Source name.
    :param source_folder: Source folder.
    """
    if interval_min is None:
        interval_min = 3600
    catalog_spec = get_catalog_spec(runtime, source_folder, archive_folder, source_name)
    all_items = list_catalog(
        runtime,
        catalog_spec,
        date_min=date_min,
        date_max=date_max,
        age_min=age_min,
        age_max=age_max,
        tags=tags,
    )
    kept_names = [
        item.display_name
        for item in list_catalog(
            runtime,
            catalog_spec,
            date_min=date_min,
            date_max=date_max,
            age_min=age_min,
            age_max=age_max,
            interval_min=interval_min,
            interval_max=interval_max,
            tags=tags,
        )
    ]
    deleted_items = [
        item
        for item in all_items
        if item.display_name not in kept_names
    ]
    deleted_names = [item.display_name for item in deleted_items]
    if deleted_names:
        with runtime.context(archive_folder=catalog_spec.archive_folder) as context:
            context.heading(1, 'items to purge from "{archive_folder}"')
            for line in format_catalog_table(all_items,
                                             flagged_names=deleted_names,
                                             flag_text='*purge*'):
                print(line)
            print('')
            if no_confirmation or context.boolean_prompt('Purge above items', default=False):
                print('')
                for deleted_item in deleted_items:
                    context.message(f'Deleting: {deleted_item.display_name}')
                    if deleted_item.path.is_dir():
                        delete_folder(deleted_item.path, quiet=True)
                    else:
                        delete_file(deleted_item.path, quiet=True)
            else:
                print('Cancelled.')
    else:
        runtime.message('There is nothing to prune.')
