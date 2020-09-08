"""Archive support for rsync targets."""

import os
from typing import List, Text

from jiig.utility.filesystem import create_folder
from tzar.archiver import archive_method

from .base import MethodData, ArchiveMethodBase


@archive_method('sync')
class ArchiveMethodSync(ArchiveMethodBase):
    def build_save_command(self, method_data: MethodData) -> List[Text]:
        create_folder(os.path.dirname(method_data.target_path))
        cmd_args = ['rsync', '-a', f'--include-from={method_data.source_list_path}']
        if method_data.verbose:
            cmd_args.append('-v')
        cmd_args.extend([f'{method_data.source_path}/', f'{method_data.target_path}/'])
        return cmd_args
