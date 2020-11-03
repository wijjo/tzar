"""Tzar prune command."""

import jiig

from tzar.internal.task_runner import TzarTaskRunner
from .arguments import ArchivePathArg


@jiig.task(
    'delete',
    ArchivePathArg(positional=True, cardinality='+'),
    description='Delete archive(s) [destructive]',
)
def task_delete(_runner: TzarTaskRunner):
    pass
