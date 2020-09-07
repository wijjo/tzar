from __future__ import annotations
from typing import Text, Iterator, Dict, Type, List, Optional, Callable

from jiig.utility.console import log_message
from tzar.methods.base import ArchiveMethodBase

METHOD_MAP: Dict[Text, Type[ArchiveMethodBase]] = {}
DEFAULT_METHOD: Optional[Text] = None


class Archiver:

    def __init__(self,
                 method: ArchiveMethodBase,
                 method_name: Text,
                 dry_run: bool = False):
        self._method = method
        self.method_name = method_name
        self.dry_run = dry_run

    def save(self,
             source_paths: Iterator[Text],
             target_path: Text,
             verbose: bool = False,
             progress: bool = False):
        if self.dry_run:
            log_message(f'Saving archive "{target_path}" (dry run):')
            for path in source_paths:
                log_message(f'  {path}')
        else:
            self._method.save(source_paths,
                              target_path,
                              verbose=verbose,
                              progress=progress)


def archive_method(name: Text, is_default: bool = False) -> Callable:

    def _inner(method_cls: Type[ArchiveMethodBase]):
        METHOD_MAP[name] = method_cls
        if is_default:
            global DEFAULT_METHOD
            DEFAULT_METHOD = name
        return method_cls
    return _inner


def get_method_names() -> List[Text]:
    return list(sorted(METHOD_MAP.keys()))


def create_archiver(method_name: Text, dry_run: bool = False) -> Archiver:
    if method_name not in METHOD_MAP:
        raise RuntimeError(f'Bad archive method name "{method_name}".')
    return Archiver(METHOD_MAP[method_name](), method_name, dry_run=dry_run)
