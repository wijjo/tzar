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
Generic archiver to drive selected archive method.
"""

import os
from dataclasses import dataclass
from pathlib import Path
from tempfile import NamedTemporaryFile
from time import strftime, struct_time, localtime
from typing import Sequence, Iterator, Collection

from jiig.runtime import Runtime
from jiig.util.log import abort, log_error, log_message, log_warning
from jiig.util.filesystem import create_folder, short_path, iterate_filtered_files, \
    temporary_working_folder
from jiig.util.text.human_units import format_human_byte_count
from jiig.util.process import shell_command_string

from . import methods

from .archive_method import MethodListItem, MethodSaveData
from .constants import TIMESTAMP_FORMAT
from .discovered_archive import DiscoveredArchive


@dataclass
class CatalogItem:
    """Data for a catalog archive."""
    method_name: str
    path: Path
    tags: list[str]
    size: int
    time: float

    @property
    def time_struct(self) -> struct_time:
        return localtime(self.time)

    @property
    def time_string(self) -> str:
        return strftime('%Y-%m-%d %H:%M.%S', self.time_struct)


def _tags_from_string(tags: str = None) -> Iterator[str]:
    if tags:
        for tag in tags.split(','):
            if tag.isalnum():
                yield tag
            else:
                log_error(f'Bad non-alphanumeric archive tag "{tag}".')


class TzarRuntime(Runtime):

    def list_archive(self,
                     archive_path: str | Path,
                     ) -> Sequence[MethodListItem]:
        """
        List tarball contents.

        :param archive_path: archive tarball file path
        :return: sequence of archive items
        """
        try:
            discovered_archive = DiscoveredArchive.new(archive_path)
            return discovered_archive.method_cls().handle_list(archive_path)
        except ValueError as exc:
            self.abort(exc)

    @staticmethod
    def get_method_names() -> list[str]:
        """Provide method name list, e.g. for method option help text."""
        return list(sorted(methods.METHOD_MAP.keys()))

    def save_archive(self,
                     source_folder: str | Path,
                     archive_folder: str | Path,
                     method_name: str,
                     source_name: str = None,
                     tags: str = None,
                     pending: bool = False,
                     gitignore: bool = False,
                     excludes: list[str] = None,
                     timestamp: bool = False,
                     progress: bool = False,
                     keep_list: bool = False):
        """
        Save an archive of a source folder.

        :param source_folder: source folder path
        :param archive_folder: archive folder path
        :param method_name: archive method name
        :param source_name: optional source name (default: folder name)
        :param tags: optional tags to assign to archive (added to file name)
        :param pending: locally-modified source repository files only if True
        :param gitignore: obey .gitignore exclusions if True
        :param excludes: file exclusion patterns
        :param timestamp: assign time stamp to archive (added to file name)
        :param progress: show progress if True
        :param keep_list: do not delete temporary file list file if True
        """
        if not isinstance(source_folder, Path):
            source_folder = Path(source_folder)
        if not isinstance(archive_folder, Path):
            archive_folder = Path(archive_folder)
        if source_name is None:
            source_name = source_folder.name
        method_cls = methods.METHOD_MAP.get(method_name)
        if not method_cls:
            raise RuntimeError(f'Bad archive method name "{method_name}".')
        create_folder(archive_folder)
        # Temporarily relocate in order to resolve relative paths.
        with temporary_working_folder(source_folder):
            name_parts = [source_name]
            if timestamp:
                name_parts.append(strftime(TIMESTAMP_FORMAT))
            if tags:
                name_parts.extend(tags)
            full_folder_path = archive_folder / '_'.join(name_parts)
            source_file_iterator = iterate_filtered_files(source_folder,
                                                          pending=pending,
                                                          gitignore=gitignore,
                                                          excludes=excludes)
            if self.options.dry_run:
                for path_idx, path in enumerate(source_file_iterator):
                    if path_idx == 0:
                        log_message(f'Saving archive (dry run)'
                                    f': {short_path(full_folder_path)}')
                    log_message(f'  {path}')
                return
            # Save and flush the file path list as a temporary file in order to
            # immediately feed it to the archive method command.
            temp_options = {}
            if keep_list:
                temp_options['delete'] = False
                temp_options['dir'] = '/tmp'
            total_files = 0
            total_folders = 0
            total_bytes = 0
            visited_folders: set[str] = set()
            with NamedTemporaryFile(prefix=f'tzar_{source_folder.name}_',
                                    suffix='.txt',
                                    mode='w',
                                    encoding='utf-8',
                                    **temp_options) as temp_file:
                if keep_list:
                    log_message(f'File list: {temp_file.name}')
                for file_path in source_file_iterator:
                    if file_path.is_file():
                        temp_file.write(str(file_path))
                        temp_file.write(os.linesep)
                        total_files += 1
                        total_bytes += file_path.stat(follow_symlinks=False).st_size
                        folder_path = file_path.parent or Path('.')
                        if folder_path not in visited_folders:
                            visited_folders.add(str(folder_path))
                            total_folders += 1
                            total_bytes += folder_path.stat(follow_symlinks=False).st_size
                    else:
                        log_warning('Source path is not a file.', file_path)
                temp_file.flush()
                method_data = MethodSaveData(
                    source_path=source_folder,
                    source_list_path=Path(temp_file.name),
                    archive_path=full_folder_path,
                    verbose=self.options.verbose and not progress,
                    dry_run=self.options.dry_run,
                    progress=progress,
                    total_bytes=total_bytes,
                    total_files=total_files,
                    total_folders=total_folders,
                )
                save_data = method_cls.handle_save(method_data)
                log_message(f'Saving archive: {short_path(save_data.archive_path)}')
                full_command = shell_command_string(*save_data.command_arguments)
                if self.options.verbose:
                    log_message('Archive command:', full_command)
                formatted_bytes = format_human_byte_count(total_bytes, unit_format='b')
                log_message(f'Archiving {formatted_bytes}'
                            f' from {total_files} files'
                            f' in {total_folders} folders ...')
                ret_code = os.system(full_command)
                if ret_code != 0:
                    abort('Archive command failed.', full_command)

    def list_catalog(self,
                     source_folder: str | Path,
                     archive_folder: str | Path,
                     source_name: str = None,
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

        :param source_folder: source folder path
        :param archive_folder: archive folder path
        :param source_name: optional source name (default: folder name)
        :param date_min: timestamp based on minimum date
        :param date_max: timestamp based on maximum date
        :param age_min: timestamp based on minimum age
        :param age_max: timestamp based on maximum age
        :param interval_min: minimum seconds between archive saves (ignored if smaller)
        :param interval_max: maximum seconds between archive saves (ignored if larger)
        :param tags: optional tags for filtering catalog archives (all are required)
        :return: found catalog items
        """
        if not isinstance(source_folder, Path):
            source_folder = Path(source_folder)
        if not isinstance(archive_folder, Path):
            archive_folder = Path(archive_folder)
        if source_name is None:
            source_name = source_folder.name
        timestamp_min = max(filter(lambda ts: ts is not None, (date_min, age_max)),
                            default=None)
        timestamp_max = min(filter(lambda ts: ts is not None, (date_max, age_min)),
                            default=None)
        if not archive_folder.is_dir():
            self.error('Catalog archive folder does not exist.', archive_folder)
            return []
        if not source_folder.is_dir():
            self.error(f'Source folder does not exist.', source_folder)
            return []
        discovered_archives: list[DiscoveredArchive] = []
        for path in archive_folder.glob('*'):
            try:
                discovered_archives.append(DiscoveredArchive.new(path))
            except ValueError as exc:
                log_error(exc)
        if tags:
            filter_tag_set = set(tags)
        else:
            filter_tag_set = None
        return self.build_catalog_list(discovered_archives,
                                       source_name,
                                       timestamp_min=timestamp_min,
                                       timestamp_max=timestamp_max,
                                       interval_min=interval_min,
                                       interval_max=interval_max,
                                       filter_tag_set=filter_tag_set)

    @staticmethod
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
        :return:
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
