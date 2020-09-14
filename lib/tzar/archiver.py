"""Generic archiver to drive selected archive method."""

import os
import re
from dataclasses import dataclass
from tempfile import NamedTemporaryFile
from time import strftime, mktime, struct_time, localtime
from typing import Text, Dict, Type, List, Optional, Callable, Set, Sequence

from jiig.utility.console import abort, log_error, log_message, log_warning
from jiig.utility.filesystem import chdir, create_folder, short_path, iterate_filtered_files
from jiig.utility.general import format_byte_count
from jiig.utility.process import shell_command_string

from tzar.constants import TARGET_TIMESTAMP, DEFAULT_ARCHIVE_FOLDER, ARCHIVE_NAME_PATTERN
from tzar.methods.base import MethodSaveData, ArchiveMethodBase, MethodListItem


@dataclass
class RegisteredMethod:
    """Data for registered archive method."""
    name: Text
    method_cls: Type[ArchiveMethodBase]


METHOD_MAP: Dict[Text, RegisteredMethod] = {}
DEFAULT_METHOD: Optional[Text] = None


@dataclass
class ApplicableMethod:
    """Data for method chosen based on file name."""
    method_name: Text
    file_name: Text
    method_cls: Type[ArchiveMethodBase]


@dataclass
class CatalogItem:
    """Data for a catalog archive."""
    method_name: Text
    file_name: Text
    folder: Text
    comment: Text
    size: int
    time: float

    @property
    def file_path(self) -> Text:
        return os.path.join(self.folder, self.file_name)

    @property
    def time_struct(self) -> struct_time:
        return localtime(self.time)

    @property
    def time_string(self) -> Text:
        return strftime('%Y-%m-%d %H:%M.%S', self.time_struct)


class Archiver:
    """Archiver class is responsible for archive catalogs and operations."""

    def __init__(self,
                 archive_folder: Text = None,
                 verbose: bool = False,
                 dry_run: bool = False
                 ):
        self.archive_folder = os.path.abspath(archive_folder or DEFAULT_ARCHIVE_FOLDER)
        self.verbose = verbose
        self.dry_run = dry_run

    def save_archive(self,
                     source_folder: Text,
                     method_name: Text,
                     pending: bool = False,
                     gitignore: bool = False,
                     excludes: List[Text] = None,
                     timestamp: bool = False,
                     progress: bool = False,
                     keep_list: bool = False):
        registered_method = METHOD_MAP.get(method_name)
        if not registered_method:
            raise RuntimeError(f'Bad archive method name "{method_name}".')
        create_folder(self.archive_folder)
        # Temporarily relocate in order to resolve relative paths.
        with chdir(source_folder):
            name_parts = [os.path.basename(os.getcwd())]
            if timestamp:
                name_parts.append(strftime(TARGET_TIMESTAMP))
            full_folder_path = os.path.join(self.archive_folder, '_'.join(name_parts))
            source_file_iterator = iterate_filtered_files(source_folder,
                                                          pending=pending,
                                                          gitignore=gitignore,
                                                          excludes=excludes)
            if self.dry_run:
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
            visited_folders: Set[Text] = set()
            with NamedTemporaryFile(prefix=f'tzar_{os.path.basename(source_folder)}_',
                                    suffix='.txt',
                                    mode='w',
                                    encoding='utf-8',
                                    **temp_options) as temp_file:
                if keep_list:
                    log_message(f'File list: {temp_file.name}')
                for file_path in source_file_iterator:
                    if os.path.isfile(file_path):
                        temp_file.write(file_path)
                        temp_file.write(os.linesep)
                        total_files += 1
                        total_bytes += os.stat(file_path, follow_symlinks=False).st_size
                        folder_path = os.path.dirname(file_path) or '.'
                        if folder_path not in visited_folders:
                            visited_folders.add(folder_path)
                            total_folders += 1
                            total_bytes += os.stat(folder_path, follow_symlinks=False).st_size
                    else:
                        log_warning('Source path is not a file.', file_path)
                temp_file.flush()
                method_data = MethodSaveData(source_path=source_folder,
                                             source_list_path=temp_file.name,
                                             archive_path=full_folder_path,
                                             verbose=self.verbose and not progress,
                                             dry_run=self.dry_run,
                                             progress=progress,
                                             total_bytes=total_bytes,
                                             total_files=total_files,
                                             total_folders=total_folders)
                save_data = registered_method.method_cls.handle_save(method_data)
                log_message(f'Saving archive: {short_path(save_data.archive_path)}')
                full_command = shell_command_string(*save_data.command_arguments)
                if self.verbose:
                    log_message('Archive command:', full_command)
                formatted_bytes = format_byte_count(total_bytes,
                                                    decimal_places=1,
                                                    binary_units=True)
                log_message(f'Archiving {formatted_bytes}'
                            f' from {total_files} files'
                            f' in {total_folders} folders ...')
                ret_code = os.system(full_command)
                if ret_code != 0:
                    abort('Archive command failed.', full_command)

    @classmethod
    def list_archive(cls, archive_path: Text) -> Sequence[MethodListItem]:
        """
        List tarball contents.

        :param archive_path: archive tarball file path
        :return: sequence of archive items
        """
        registered_method = cls.method_for_archive(archive_path)
        if not registered_method:
            abort(f'Unsupported archive.', archive_path)
        return registered_method.method_cls().handle_list(archive_path)

    @classmethod
    def method_for_archive(cls, archive_path: Text) -> Optional[ApplicableMethod]:
        """
        Determine archive method based on file name.

        :param archive_path: path to archive
        :return: method object or None if the file/folder is not an archive
        """
        for registered_method in METHOD_MAP.values():
            base_path = registered_method.method_cls.check_supported(archive_path)
            if base_path:
                return ApplicableMethod(method_name=registered_method.name,
                                        method_cls=registered_method.method_cls,
                                        file_name=os.path.basename(base_path))
        return None

    def list_catalog(self, source_folder: Text) -> List[CatalogItem]:
        """
        List catalog archives.

        :param source_folder: source folder for filtering archives
        :return: found catalog items
        """
        if not os.path.isdir(self.archive_folder):
            log_error(f'Catalog folder does not exist.', self.archive_folder)
            return []
        if not source_folder:
            source_folder = os.getcwd()
        if not os.path.isdir(source_folder):
            log_error(f'Source folder does not exist.', source_folder)
            return []
        source_name = os.path.basename(source_folder)
        pattern = ARCHIVE_NAME_PATTERN.format(name=source_name)
        matcher = re.compile(pattern)
        items: List[CatalogItem] = []
        with chdir(self.archive_folder, quiet=True):
            for file_name in os.listdir(self.archive_folder):
                # First see if there's a method to handle it.
                archive_path = os.path.join(self.archive_folder, file_name)
                applicable_method = self.method_for_archive(archive_path)
                if applicable_method:
                    # Then check if it matches the naming pattern.
                    matched = matcher.match(applicable_method.file_name)
                    if matched:
                        file_stat = os.stat(file_name)
                        time_string = matched.group(2)
                        if time_string:
                            file_time = mktime((int(matched.group('year')),
                                                int(matched.group('month')),
                                                int(matched.group('day')),
                                                int(matched.group('hours')),
                                                int(matched.group('minutes')),
                                                int(matched.group('seconds')),
                                                0, 0, -1))
                        else:
                            file_time = file_stat.st_mtime,
                        items.append(CatalogItem(file_name=file_name,
                                                 method_name=applicable_method.method_name,
                                                 folder=self.archive_folder,
                                                 comment=matched.group('comment') or '',
                                                 size=file_stat.st_size,
                                                 time=file_time))
        return sorted(items, key=lambda item: item.time, reverse=True)


def archive_method(name: Text, is_default: bool = False,) -> Callable:
    """Archive method class decorator.
    :param name: method name
    :param is_default: default method if True
    """

    def _inner(method_cls: Type[ArchiveMethodBase]):
        METHOD_MAP[name] = RegisteredMethod(name, method_cls)
        if is_default:
            global DEFAULT_METHOD
            DEFAULT_METHOD = name
        return method_cls
    return _inner


def get_method_names() -> List[Text]:
    """Provide method name list, e.g. for method option help text."""
    return list(sorted(METHOD_MAP.keys()))


def create_archiver(archive_folder: Text = None,
                    verbose: bool = False,
                    dry_run: bool = False
                    ) -> Archiver:
    """Factory function to create Archiver for chosen method."""
    return Archiver(archive_folder=archive_folder,
                    verbose=verbose,
                    dry_run=dry_run)
