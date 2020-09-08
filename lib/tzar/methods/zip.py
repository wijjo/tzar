"""Support for Zip archives."""

from typing import List, Text

from tzar.archiver import archive_method

from .base import MethodData, ArchiveMethodBase


@archive_method('zip', file_extension='zip')
class ArchiveMethodZip(ArchiveMethodBase):
    def build_save_command(self, method_data: MethodData) -> List[Text]:
        cmd_args = ['zip', '-r', '-', '.', f'-i@{method_data.source_list_path}']
        if not method_data.verbose:
            cmd_args.append('-q')
        if method_data.pv_progress:
            cmd_args.extend(['|', 'pv', '-bret'])
        cmd_args.extend(['>', method_data.target_path])
        return cmd_args
