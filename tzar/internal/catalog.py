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

"""Catalog utility functions and classes."""

import os
from dataclasses import dataclass
from pathlib import Path
from time import (
    strftime,
    struct_time,
    localtime,
)
from typing import (
    Collection,
    Iterable,
    Iterator,
)

from jiig import Runtime
from jiig.util.filesystem import (
    format_file_size,
    short_path,
)
from jiig.util.log import log_error
from jiig.util.text.table import format_table

from .archive import (
    CatalogSpec,
    DiscoveredArchive,
    get_timestamp_matcher,
)


@dataclass
class CatalogItem:
    """Data for a catalog archive."""
    path: Path
    method_name: str
    tags: list[str]
    size: int
    time: float

    @property
    def time_struct(self) -> struct_time:
        return localtime(self.time)

    @property
    def time_string(self) -> str:
        return strftime('%Y-%m-%d %H:%M.%S', self.time_struct)

    @property
    def display_name(self) -> str:
        return short_path(self.path.name, is_folder=os.path.isdir(self.path))


def get_catalog_spec(runtime: Runtime,
                     source_folder: str | Path,
                     archive_folder: str | Path = None,
                     source_name: str = None,
                     ) -> CatalogSpec:
    """
    Get archive folder path or default.

    If the default folder is provided, calculates a nested path within it based
    on the working folder.

    :param runtime: Jiig runtime API.
    :param source_folder: source folder path
    :param archive_folder: archive folder path (default: tzar catalog sub-folder)
    :param source_name: Source name (default: source folder name).
    :return: archive folder path
    """
    default_archive_folder = str(runtime.get_param('archive_folder'))
    if isinstance(source_folder, str):
        source_folder = Path(source_folder)
    elif source_folder is None:
        source_folder = Path(os.getcwd())
    if isinstance(archive_folder, str):
        archive_folder = Path(archive_folder)
    elif isinstance(archive_folder, Path):
        pass
    else:
        home_path = Path.home()
        if source_folder.is_relative_to(home_path):
            sub_path = source_folder.relative_to(home_path)
        else:
            sub_path = Path('__ROOT__') / source_folder
        archive_folder = Path(default_archive_folder).expanduser() / sub_path
    if source_name is None:
        source_name = archive_folder.name
    return CatalogSpec(source_folder, archive_folder, source_name)


def list_catalog(runtime: Runtime,
                 catalog_spec: CatalogSpec,
                 date_min: float = None,
                 date_max: float = None,
                 age_min: float = None,
                 age_max: float = None,
                 interval_min: float = None,
                 interval_max: float = None,
                 tags: Collection[str] = None,
                 ) -> list[CatalogItem]:
    """
    List catalog archives.

    :param runtime: Jiig runtime API.
    :param catalog_spec: source folder, archive folder, and source name
    :param date_min: timestamp based on minimum date
    :param date_max: timestamp based on maximum date
    :param age_min: timestamp based on minimum age
    :param age_max: timestamp based on maximum age
    :param interval_min: minimum seconds between archive saves (ignored if smaller)
    :param interval_max: maximum seconds between archive saves (ignored if larger)
    :param tags: optional tags for filtering catalog archives (all are required)
    :return: found catalog items
    """
    timestamp_matcher = get_timestamp_matcher(str(runtime.get_param('timestamp_format')))
    timestamp_min = max(filter(lambda ts: ts is not None, (date_min, age_max)),
                        default=None)
    timestamp_max = min(filter(lambda ts: ts is not None, (date_max, age_min)),
                        default=None)
    if not catalog_spec.archive_folder.is_dir():
        log_error('Catalog archive folder does not exist.', catalog_spec.archive_folder)
        return []
    if not catalog_spec.source_folder.is_dir():
        log_error(f'Source folder does not exist.', catalog_spec.source_folder)
        return []
    discovered_archives: list[DiscoveredArchive] = []
    for path in catalog_spec.archive_folder.glob('*'):
        try:
            discovered_archive = DiscoveredArchive.get(path, timestamp_matcher)
            if discovered_archive is not None:
                discovered_archives.append(discovered_archive)
        except ValueError as exc:
            log_error(exc)
    if tags:
        filter_tag_set = set(tags)
    else:
        filter_tag_set = None
    return build_catalog_list(discovered_archives,
                              catalog_spec.source_name,
                              timestamp_min=timestamp_min,
                              timestamp_max=timestamp_max,
                              interval_min=interval_min,
                              interval_max=interval_max,
                              filter_tag_set=filter_tag_set)


def build_catalog_list(archives: list[DiscoveredArchive],
                       source_name: str,
                       timestamp_min: float = None,
                       timestamp_max: float = None,
                       interval_min: float = None,
                       interval_max: float = None,
                       filter_tag_set: set[str] | None = None,
                       ) -> list[CatalogItem]:
    """
    General function for building archive catalog lists.

    Separated this method out to allow testing with synthetic data.

    :param archives: discovered archives (file information)
    :param source_name: source name for identifying related archives
    :param timestamp_min: earliest time stamp to accept
    :param timestamp_max: latest time stamp to accept
    :param interval_min: minimum seconds between archive saves (ignored if smaller)
    :param interval_max: maximum seconds between archive saves (ignored if larger)
    :param filter_tag_set: optional required tags
    :return: catalog item list
    """
    items: list[CatalogItem] = []
    for archive in archives:
        if ((archive.source_name == source_name)
                and (timestamp_min is None or archive.time_stamp >= timestamp_min)
                and (timestamp_max is None or archive.time_stamp <= timestamp_max)
                and (filter_tag_set is None or filter_tag_set.issubset(archive.tags))):
            items.append(CatalogItem(path=archive.path,
                                     method_name=archive.method_name,
                                     tags=archive.tags,
                                     size=archive.file_size,
                                     time=archive.time_stamp))
    # Sort by time descending and filter by any interval limits provided.
    if items:
        items.sort(key=lambda x: x.time, reverse=True)
        if interval_min is not None or interval_max is not None:
            filtered_items: list[CatalogItem] = [items[0]]
            for item_idx, item in enumerate(items[1:], start=1):
                delta_time = items[item_idx - 1].time - item.time
                if ((interval_min is None or delta_time >= interval_min)
                        and (interval_max is None or delta_time <= interval_max)):
                    filtered_items.append(item)
            items = filtered_items
    return items


def format_catalog_table(items: Iterable[CatalogItem],
                         unit_format: str = 'b',
                         flagged_names: Iterable[str] = None,
                         flag_text: str = None,
                         ) -> Iterator[str]:
    """
    Format catalog item table for listing.

    :param items: catalog items
    :param unit_format: 'b' for KiB/MiB/... or 'd' for KB/MB/... (default: 'b')
    :param flagged_names: optional display names to flag (default: no flagged items)
    :param flag_text: optional flag text (default: '*')
    :return: text line iterator
    """
    if flag_text is None:
        flag_text = '*'
    headers = ['date/time', 'method', 'tags', 'size', 'archive name']
    item_list = list(items)
    rows = [
        (
            item.time_string,
            item.method_name,
            ','.join(item.tags),
            format_file_size(item.size, unit_format=unit_format),
            item.display_name,
        )
        for item in items
    ]
    for idx, line in enumerate(format_table(*rows, headers=headers)):
        # Account for 2 heading lines.
        if idx >= 2 and flagged_names and item_list[idx-2].display_name in flagged_names:
            line += f'  {flag_text}'
        yield line
