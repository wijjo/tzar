"""Tzar prune command."""

from typing import Text, List

from jiig import Task, Arg, adapters


class TaskClass(Task):
    """Delete archive(s) [destructive]."""

    # For type inspection only.
    class Data:
        ARCHIVE_PATH: List[Text]
    data: Data

    args = [
        Arg('ARCHIVE_PATH', 'Path(s) to source archive file or folder',
            adapters.path.check_exists,
            cardinality='+'),
    ]

    def on_run(self):
        pass
