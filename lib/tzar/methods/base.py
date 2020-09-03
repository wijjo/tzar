"""Archive support base class."""

from typing import Text, Iterator


class ArchiveMethodBase:
    def save(self, source_paths: Iterator[Text], target_path: Text):
        raise NotImplementedError
