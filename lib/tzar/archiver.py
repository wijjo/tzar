"""Generic archiver to drive selected archive method."""

import os
from dataclasses import dataclass
from tempfile import NamedTemporaryFile
from typing import Text, Dict, Type, List, Optional, Callable

from jiig.utility.console import abort, log_message, log_warning
from jiig.utility.filesystem import short_path, iterate_filtered_files
from jiig.utility.process import shell_command_string
from tzar.methods.base import MethodData, ArchiveMethodBase


@dataclass
class RegisteredMethod:
    """Data for registered archive method."""
    name: Text
    method_cls: Type[ArchiveMethodBase]
    file_extension: Text


METHOD_MAP: Dict[Text, RegisteredMethod] = {}
DEFAULT_METHOD: Optional[Text] = None


class Archiver:
    """Archiver class drives archiving activity using the selected method."""

    def __init__(self,
                 registered_method: RegisteredMethod,
                 dry_run: bool = False,
                 pending: bool = False,
                 gitignore: bool = False,
                 excludes: List[Text] = None
                 ):
        self._method = registered_method.method_cls()
        self.method_name = registered_method.name
        self.file_extension = registered_method.file_extension
        self.dry_run = dry_run
        self.pending = pending
        self.gitignore = gitignore
        self.excludes = excludes

    def save(self,
             source_folder: Text,
             target_path: Text,
             verbose: bool = False,
             progress: bool = False,
             keep_list: bool = False):
        source_file_iterator = iterate_filtered_files(source_folder,
                                                      pending=self.pending,
                                                      gitignore=self.gitignore,
                                                      excludes=self.excludes)
        if self.file_extension:
            full_target_path = '.'.join([target_path, self.file_extension])
        else:
            full_target_path = target_path
        if self.dry_run:
            for path_idx, path in enumerate(source_file_iterator):
                if path_idx == 0:
                    log_message(f'Saving archive (dry run): {short_path(full_target_path)}')
                log_message(f'  {path}')
            return
        log_message(f'Saving archive: {short_path(full_target_path)}')
        # Save and flush the file path list as a temporary file in order to
        # immediately feed it to the archive method command.
        temp_options = {}
        if keep_list:
            temp_options['delete'] = False
            temp_options['dir'] = '/tmp'
        with NamedTemporaryFile(prefix=f'tzar_{os.path.basename(source_folder)}_',
                                suffix='.txt',
                                mode='w',
                                encoding='utf-8',
                                **temp_options) as temp_file:
            if keep_list:
                log_message(f'File list: {temp_file.name}')
            total_bytes = 0
            for source_path in source_file_iterator:
                if os.path.isfile(source_path):
                    temp_file.write(source_path)
                    temp_file.write(os.linesep)
                    total_bytes += os.stat(source_path, follow_symlinks=False).st_size
                else:
                    log_warning('Source path is not a file.', source_path)
            temp_file.flush()
            method_data = MethodData(source_path=source_folder,
                                     source_list_path=temp_file.name,
                                     target_path=full_target_path,
                                     verbose=verbose and not progress,
                                     dry_run=self.dry_run,
                                     progress=progress,
                                     total_bytes=total_bytes)
            cmd_args = self._method.build_save_command(method_data)
            full_command = shell_command_string(*cmd_args)
            if verbose:
                log_message('Archive command:', full_command)
            ret_code = os.system(full_command)
            if ret_code != 0:
                abort('Archive command failed.', full_command)


def archive_method(name: Text,
                   file_extension: Text = None,
                   is_default: bool = False,
                   ) -> Callable:
    """Archive method class decorator.
    :param name: method name
    :param file_extension: archive file extension
    :param is_default: default method if True
    """

    def _inner(method_cls: Type[ArchiveMethodBase]):
        METHOD_MAP[name] = RegisteredMethod(name, method_cls, file_extension)
        if is_default:
            global DEFAULT_METHOD
            DEFAULT_METHOD = name
        return method_cls
    return _inner


def get_method_names() -> List[Text]:
    """Provide method name list, e.g. for method option help text."""
    return list(sorted(METHOD_MAP.keys()))


def create_archiver(method_name: Text,
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
                    dry_run=dry_run,
                    pending=pending,
                    gitignore=gitignore,
                    excludes=excludes)
