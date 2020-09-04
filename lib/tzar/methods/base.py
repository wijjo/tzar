"""Archive support base class."""

from typing import Text, Iterator


class ArchiveMethodBase:
    def save(self,
             source_paths: Iterator[Text],
             target_path: Text,
             verbose: bool = False,
             progress: bool = False):
        raise NotImplementedError
