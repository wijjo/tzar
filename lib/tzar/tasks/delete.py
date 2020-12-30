"""Tzar prune command."""

from tzar.internal.tzar_task import TzarTask

from . import arguments


class TaskClass(TzarTask):
    """Delete archive(s) [destructive]."""
    args = [
        arguments.archive_path_argument(cardinality='+'),
    ]

    def on_run(self):
        pass
