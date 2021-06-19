"""Tzar delete command."""

import jiig

from tzar import arguments
from tzar.runtime import TzarRuntime


class Task(jiig.Task):
    """Delete archive(s) [destructive]."""

    archive_path: arguments.archive_paths_argument

    def on_run(self, _runtime: TzarRuntime):
        raise NotImplementedError
