"""Tzar compare command."""

import jiig

from tzar.internal.task_runner import TzarTaskRunner
from .arguments import SourceFolderArg, ArchivePathArg


@jiig.task(
    'compare',
    SourceFolderArg(),
    ArchivePathArg(positional=True),
    description='Compare archive to existing files',
)
def task_compare(_runner: TzarTaskRunner):
    pass
