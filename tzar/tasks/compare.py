"""Tzar compare command."""

import jiig

from tzar import constants
from tzar.runtime import TzarRuntime


# noinspection PyUnusedLocal
@jiig.task(
    cli={
        'options': {
            'source_folder': constants.OPTION_SOURCE_FOLDER,
        }
    }
)
def compare(
    runtime: TzarRuntime,
    archive_path: jiig.f.filesystem_object(exists=True),
    source_folder: jiig.f.filesystem_folder(absolute_path=True) = '.',
):
    """
    Compare archive to existing files.

    :param runtime: Jiig runtime API.
    :param archive_path: Path to source archive file or folder.
    :param source_folder: Source folder.
    """
    raise NotImplementedError
