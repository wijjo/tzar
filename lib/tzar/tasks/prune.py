"""
Tzar prune command.

Pruning options provide flexibility for specifying different algorithms for
choosing which archives to purge.

Due to the destructive nature of these actions, an action summary is displayed,
followed by a confirmation prompt. A NO_CONFIRMATION option can disable the
confirmation prompt, e.g. for automation scripts.
"""

import jiig

from tzar.internal.task_runner import TzarTaskRunner
from .arguments import AgeMaxArg, AgeMinArg, ArchiveFolderArg, DateMaxArg, DateMinArg, \
    IntervalMaxArg, IntervalMinArg, NoConfirmationArg, SourceNameArg, SourceFolderArg, TagsArg


@jiig.task(
    'prune',
    AgeMaxArg(),
    AgeMinArg(),
    ArchiveFolderArg(),
    DateMaxArg(),
    DateMinArg(),
    IntervalMaxArg(),
    IntervalMinArg(),
    NoConfirmationArg(),
    SourceNameArg(),
    SourceFolderArg(),
    TagsArg(),
    description='Prune archives to save space [destructive]',
)
def task_prune(runner: TzarTaskRunner):
    for item in runner.list_catalog():
        print('-->', item.time_string)
