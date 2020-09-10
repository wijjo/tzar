"""Archive support for file-based cloning using rsync."""

import os

from jiig.utility.filesystem import create_folder
from tzar.archiver import archive_method

from .base import MethodData, ArchiveMethodBase, MethodSaveData


@archive_method('files')
class ArchiveMethodSync(ArchiveMethodBase):
    def handle_save(self, method_data: MethodData) -> MethodSaveData:
        create_folder(os.path.dirname(method_data.target_path))
        cmd_args = ['rsync', '-a', f'--include-from={method_data.source_list_path}']
        if method_data.verbose:
            cmd_args.append('-v')
        cmd_args.extend([f'{method_data.source_path}/', f'{method_data.target_path}/'])
        return MethodSaveData(target_path=method_data.target_path, command_arguments=cmd_args)
