"""Archive support base class."""

from dataclasses import dataclass
from typing import List, Text

from jiig.utility.console import log_warning
from jiig.utility.filesystem import find_system_program

PV_INSTALLED = bool(find_system_program('pv'))
PV_WARNED = False


@dataclass
class MethodData:
    source_path: Text
    source_list_path: Text
    target_path: Text
    verbose: bool
    dry_run: bool
    progress: bool
    total_bytes: int
    total_files: int
    total_folders: int

    @property
    def pv_progress(self) -> bool:
        """
        Use instead of `progress` member when "pv" is required.

        :return: True if progress is required and pv is available
        """
        if not self.progress:
            return False
        if not PV_INSTALLED:
            global PV_WARNED
            if not PV_WARNED:
                log_warning('Please install the "pv" program in order'
                            ' to use the progress option.')
                PV_WARNED = True
            return False
        return True


@dataclass
class MethodSaveData:
    target_path: Text
    command_arguments: List[Text]


class ArchiveMethodBase:
    """Base archive method class."""

    def handle_save(self, method_data: MethodData) -> MethodSaveData:
        raise NotImplementedError
