"""Archive support package."""

from typing import Text, Dict, Type

from tzar.archive_method import ArchiveMethodBase

from .files import ArchiveMethodSync
from .gz import ArchiveMethodGZ
from .xz import ArchiveMethodXZ
from .zip import ArchiveMethodZip

METHOD_MAP: Dict[Text, Type[ArchiveMethodBase]] = {
    'files': ArchiveMethodSync,
    'gz': ArchiveMethodGZ,
    'xz': ArchiveMethodXZ,
    'zip': ArchiveMethodZip,
}

DEFAULT_METHOD = 'gz'
