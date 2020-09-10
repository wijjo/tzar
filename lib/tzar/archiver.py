"""Generic archiver to drive selected archive method."""

import os
from dataclasses import dataclass
from tempfile import NamedTemporaryFile
from time import strftime
from typing import Text, Dict, Type, List, Optional, Callable, Set

from jiig.utility.console import abort, log_message, log_warning
from jiig.utility.filesystem import chdir, create_folder, short_path, iterate_filtered_files
from jiig.utility.general import format_byte_count
from jiig.utility.process import shell_command_string
from tzar.constants import DEFAULT_TARGET
from tzar.methods.base import MethodData, ArchiveMethodBase


@dataclass
class RegisteredMethod:
    """Data for registered archive method."""
    name: Text
    method_cls: Type[ArchiveMethodBase]


METHOD_MAP: Dict[Text, RegisteredMethod] = {}
DEFAULT_METHOD: Optional[Text] = None


class Archiver:
    """Archiver class drives archiving activity using the selected method."""

    def __init__(self,
                 registered_method: RegisteredMethod,
                 target_spec: Text = None,
                 verbose: bool = False,
                 dry_run: bool = False,
                 pending: bool = False,
                 gitignore: bool = False,
                 excludes: List[Text] = None
                 ):
        self.method = registered_method.method_cls()
        self.method_name = registered_method.name
        self.target_spec = target_spec or DEFAULT_TARGET
        self.target_template = strftime(self.target_spec)
        self.verbose = verbose
        self.dry_run = dry_run
        self.pending = pending
        self.gitignore = gitignore
        self.excludes = excludes

    def save(self,
             source_folder: Text,
             progress: bool = False,
             keep_list: bool = False):
        # Temporarily change the working folder to resolve relative paths.
        with chdir(source_folder):
            target_name = os.path.basename(os.getcwd())
            relative_target_path = self.target_template.format(name=target_name)
            full_target = os.path.abspath(relative_target_path)
            create_folder(os.path.dirname(full_target))
            source_file_iterator = iterate_filtered_files(source_folder,
                                                          pending=self.pending,
                                                          gitignore=self.gitignore,
                                                          excludes=self.excludes)
            if self.dry_run:
                for path_idx, path in enumerate(source_file_iterator):
                    if path_idx == 0:
                        log_message(f'Saving archive (dry run): {short_path(full_target)}')
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
                method_data = MethodData(source_path=source_folder,
                                         source_list_path=temp_file.name,
                                         target_path=full_target,
                                         verbose=self.verbose and not progress,
                                         dry_run=self.dry_run,
                                         progress=progress,
                                         total_bytes=total_bytes,
                                         total_files=total_files,
                                         total_folders=total_folders)
                save_data = self.method.handle_save(method_data)
                log_message(f'Saving archive: {short_path(save_data.target_path)}')
                full_command = shell_command_string(*save_data.command_arguments)
                if self.verbose:
                    log_message('Archive command:', full_command)
                formatted_bytes = format_byte_count(total_bytes,
                                                    decimal_places=1,
                                                    binary_units=True)
                log_message(f'Including {formatted_bytes}'
                            f' from {total_files} files'
                            f' in {total_folders} folders ...')
                ret_code = os.system(full_command)
                if ret_code != 0:
                    abort('Archive command failed.', full_command)


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


def create_archiver(method_name: Text,
                    target_spec: Text = None,
                    verbose: bool = False,
                    dry_run: bool = False,
                    pending: bool = False,
                    gitignore: bool = False,
                    excludes: List[Text] = None
                    ) -> Archiver:
    """Factory function to create Archiver for chosen method."""
    registered_method = METHOD_MAP.get(method_name)
    if not registered_method:
        raise RuntimeError(f'Bad archive method name "{method_name}".')
    return Archiver(registered_method,
                    target_spec=target_spec,
                    verbose=verbose,
                    dry_run=dry_run,
                    pending=pending,
                    gitignore=gitignore,
                    excludes=excludes)
