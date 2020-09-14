"""Archive support base class."""

from dataclasses import dataclass
from typing import List, Text, Sequence, Optional

from jiig.utility.console import log_warning
from jiig.utility.filesystem import find_system_program

PV_INSTALLED = bool(find_system_program('pv'))
PV_WARNED = False


@dataclass
class MethodSaveData:
    """Input data for archive saving."""

    source_path: Text
    source_list_path: Text
    archive_path: Text
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
class MethodSaveResult:
    """Output data received after saving archive."""
    archive_path: Text
    command_arguments: List[Text]


@dataclass
class MethodListItem:
    """Data received for an archive file when listing archive contents."""
    path: Text
    time: float
    # File size or None if it is a folder.
    size: Optional[int]


class ArchiveMethodBase:
    """Base archive method class."""

    @classmethod
    def handle_save(cls, save_data: MethodSaveData) -> MethodSaveResult:
        """
        Required override for saving an archive.

        :param save_data: input parameters for save operation
        :return: save result data
        """
        raise NotImplementedError

    @classmethod
    def handle_list(cls, archive_path: Text) -> Sequence[MethodListItem]:
        """
        Required override for listing archive contents.

        Returned sequence may be unsorted, since it will be sorted later.

        :param archive_path: path of archive file or folder
        :return: sequence of item data objects, one per archived file
        """
        raise NotImplementedError

    @classmethod
    def check_supported(cls, archive_path: Text) -> Optional[Text]:
        """
        Required override for testing if an archive is handled by a particular method.

        :param archive_path: path of archive file or folder
        :return: base filename or path if it is handled or None if it is not
        """
        raise NotImplementedError
