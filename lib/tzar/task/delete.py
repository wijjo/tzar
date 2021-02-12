"""Tzar prune command."""

from typing import Text, List

import jiig


TASK = jiig.Task(
    description='Delete archive(s) [destructive].',
    args={
        'ARCHIVE_PATH[+]': ('Path(s) to source archive file or folder',
                            jiig.arg.path_exists),
    },
)


# For type inspection only.
class Data:
    ARCHIVE_PATH: List[Text]


@TASK.run
def task_run(_runner: jiig.Runner, _data: Data):
    raise NotImplementedError
