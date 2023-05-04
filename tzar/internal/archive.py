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

import os
from dataclasses import dataclass
from pathlib import Path
from tempfile import NamedTemporaryFile
from time import (
    mktime,
    strftime,
)
from typing import (
    Self,
    Sequence,
    Type,
)

from jiig.util.filesystem import (
    create_folder,
    iterate_filtered_files,
    iterate_git_pending,
    short_path,
    temporary_working_folder,
)
from jiig.util.log import (
    abort,
    log_message,
    log_warning,
)
from jiig.util.process import shell_command_string
from jiig.util.text.human_units import format_human_byte_count

from tzar.constants import (
    TIMESTAMP_FORMAT,
    TIMESTAMP_REGEX,
)

from .methods import (
    ArchiveMethodBase,
    ArchiveMethodGZ,
    ArchiveMethodSync,
    ArchiveMethodXZ,
    ArchiveMethodZip,
    MethodListItem,
    MethodSaveData,
)


@dataclass
class CatalogSpec:
    """Specification for catalog items."""
    source_folder: Path
    archive_folder: Path
    source_name: str


@dataclass
class ArchiveNameData:
    source_name: str
    time_stamp: float | None
    tags: list[str]


METHOD_MAP: dict[str, Type[ArchiveMethodBase]] = {
    'files': ArchiveMethodSync,
    'gz': ArchiveMethodGZ,
    'xz': ArchiveMethodXZ,
    'zip': ArchiveMethodZip,
}

METHOD_NAMES = list(sorted(METHOD_MAP.keys()))


@dataclass
class RegisteredMethod:
    """Data for registered archive method."""
    name: str
    method_cls: Type[ArchiveMethodBase]


@dataclass
class DiscoveredArchive:
    path: Path
    file_time: float
    file_size: int
    method_name: str
    method_cls: Type[ArchiveMethodBase]
    _archive_name_data: ArchiveNameData | None = None

    @property
    def archive_name(self) -> str:
        return self.method_cls.handle_get_name(self.path.name)

    @property
    def archive_name_data(self) -> ArchiveNameData:
        if self._archive_name_data is None:
            name_parts = self.archive_name.split('_')
            source_name = name_parts[0]
            # Parse name to extract date, time, and tags.
            tags: list[str] = []
            time_stamp: float | None = None
            if len(name_parts) >= 2:
                timestamp_matched = TIMESTAMP_REGEX.match(name_parts[1])
                if timestamp_matched:
                    time_stamp = mktime((
                        int(timestamp_matched.group('year')),
                        int(timestamp_matched.group('month')),
                        int(timestamp_matched.group('day')),
                        int(timestamp_matched.group('hours')),
                        int(timestamp_matched.group('minutes')),
                        int(timestamp_matched.group('seconds')),
                        0, 0, -1))
                    # Handles both comma and underscore-separated tags.
                    raw_tags = ','.join(name_parts[2:])
                else:
                    raw_tags = ','.join(name_parts[1:])
                tags = sorted(list(set([tag for tag in raw_tags.split(',') if tag.isalnum()])))
            self._archive_name_data = ArchiveNameData(source_name, time_stamp, tags)
        return self._archive_name_data

    @property
    def source_name(self) -> str:
        return self.archive_name_data.source_name

    @property
    def time_stamp(self) -> float:
        if self.archive_name_data.time_stamp is not None:
            return self.archive_name_data.time_stamp
        return self.file_time

    @property
    def tags(self) -> list[str]:
        return self.archive_name_data.tags

    @classmethod
    def get_method(cls,
                   path: str | Path,
                   assumed_type: int = None,
                   ) -> RegisteredMethod | None:
        """
        Look up archive method for file.

        :param path: path to check
        :param assumed_type: For testing, 1=file, 2=folder, None=check physical object
        :return: registered archive method or None if unsupported file type
        """
        for name, method_cls in METHOD_MAP.items():
            base_path = method_cls.check_supported(Path(path), assumed_type=assumed_type)
            if base_path:
                return RegisteredMethod(name, method_cls)
        return None

    @classmethod
    def get(cls,
            path: str | Path,
            ) -> Self | None:
        """
        Create DiscoveredArchive for physical file or folder.

        :param path: path to archive file or folder
        :return: DiscoveredArchive instance.
        :raise ValueError: when the input is not a valid archive
        """
        if not isinstance(path, Path):
            path = Path(path)
        registered_method = cls.get_method(path)
        if registered_method is None:
            return None
        file_stat = path.stat()
        return cls(path=path,
                   file_time=file_stat.st_mtime,
                   file_size=file_stat.st_size,
                   method_name=registered_method.name,
                   method_cls=registered_method.method_cls)


def list_archive(archive_path: str | Path,
                 ) -> Sequence[MethodListItem]:
    """
    List tarball contents.

    :param archive_path: archive tarball file path
    :return: sequence of archive items
    """
    try:
        discovered_archive = DiscoveredArchive.get(archive_path)
        if discovered_archive is None:
            abort(f'Unsupported archive: {archive_path}')
        return discovered_archive.method_cls().handle_list(archive_path)
    except ValueError as exc:
        abort(exc)


def save_archive(catalog_spec: CatalogSpec,
                 method_name: str,
                 tags: str = None,
                 pending: bool = False,
                 gitignore: bool = False,
                 excludes: list[str] = None,
                 timestamp: bool = False,
                 progress: bool = False,
                 keep_list: bool = False,
                 dry_run: bool = False,
                 verbose: bool = False):
    """
    Save an archive of a source folder.

    :param catalog_spec: source folder, archive folder, and source name
    :param method_name: archive method name
    :param tags: optional tags to assign to archive (added to file name)
    :param pending: locally-modified source repository files only if True
    :param gitignore: obey .gitignore exclusions if True
    :param excludes: file exclusion patterns
    :param timestamp: assign time stamp to archive (added to file name)
    :param progress: show progress if True
    :param keep_list: do not delete temporary file list file if True
    :param dry_run: avoid destructive actions if True
    :param verbose: display extra messages if True
    """
    method_cls = METHOD_MAP.get(method_name)
    if not method_cls:
        raise RuntimeError(f'Bad archive method name "{method_name}".')
    create_folder(catalog_spec.archive_folder)
    # Temporarily relocate in order to resolve relative paths.
    with temporary_working_folder(catalog_spec.source_folder):
        name_parts = [catalog_spec.source_name]
        if timestamp:
            name_parts.append(strftime(TIMESTAMP_FORMAT))
        if tags:
            name_parts.extend(tags)
        full_folder_path = catalog_spec.archive_folder / '_'.join(name_parts)
        if pending:
            source_file_iterator = iterate_git_pending(catalog_spec.source_folder)
            if gitignore or excludes:
                log_warning(f'When archiving Git pending files, the'
                            f' gitignore and excludes options are ignored.')
        else:
            source_file_iterator = iterate_filtered_files(catalog_spec.source_folder,
                                                          gitignore=gitignore,
                                                          excludes=excludes)
        if dry_run:
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
        with NamedTemporaryFile(prefix=f'tzar_{catalog_spec.source_name}_',
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
                source_path=catalog_spec.source_folder,
                source_list_path=Path(temp_file.name),
                archive_path=full_folder_path,
                verbose=verbose and not progress,
                dry_run=dry_run,
                progress=progress,
                total_bytes=total_bytes,
                total_files=total_files,
                total_folders=total_folders,
            )
            save_data = method_cls.handle_save(method_data)
            log_message(f'Saving archive: {short_path(save_data.archive_path)}')
            full_command = shell_command_string(*save_data.command_arguments)
            if verbose:
                log_message('Archive command:', full_command)
            formatted_bytes = format_human_byte_count(total_bytes, unit_format='b')
            log_message(f'Archiving {formatted_bytes}'
                        f' from {total_files} files'
                        f' in {total_folders} folders ...')
            ret_code = os.system(full_command)
            if ret_code != 0:
                abort('Archive command failed.', full_command)
