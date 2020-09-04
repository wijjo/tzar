"""Support for GZ archives."""

import os
from tempfile import NamedTemporaryFile
from typing import Text, Iterator, List, Union, Optional

from jiig.utility import log_message, log_warning, run, find_system_program, abort
from .base import ArchiveMethodBase
from tzar.archiver import archive_method


@archive_method('gz', is_default=True)
class ArchiveMethodGZ(ArchiveMethodBase):
    def save(self,
             source_paths: Iterator[Text],
             target_path: Text,
             verbose: bool = False,
             progress: bool = False):
        full_target_path = target_path + '.tar.gz'
        log_message(f'Saving {full_target_path} ...')
        # Save the file path list as a temporary that is flushed immediately
        # without closing to allow immediate reading and automatic deletion.
        with NamedTemporaryFile(mode='w') as temp_file:
            temp_file.writelines([f'{path}{os.linesep}' for path in source_paths])
            temp_file.flush()
            if progress:
                # Run tar command with pv progress reporting.
                pv_path = find_system_program('pv')
                if pv_path:
                    # TODO: Fix utility.run_shell() to handle pipes, etc..
                    command = f"tar cfz - -T '{temp_file.name}' | pv -rbt > '{full_target_path}'"
                    ret_code = os.system(command)
                    if ret_code != 0:
                        abort('Archive command failed.', command=command)
                    return
                log_warning('The "pv" program must be installed'
                            ' for the progress option to work.')
            # Run tar command without progress reporting.
            cmd_args = ['tar', 'cfz', full_target_path, '-T', temp_file.name]
            if verbose:
                cmd_args.append('-v')
            run(cmd_args)
