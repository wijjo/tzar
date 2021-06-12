"""Tzar delete command."""

import jiig

from tzar.runtime import TzarRuntime


class Task(jiig.Task):
    """Delete archive(s) [destructive]."""

    archive_path: jiig.filesystem_object(
        'Path(s) to source archive file or folder.',
        exists=True,
        repeat=(1, None))

    def on_run(self, _runtime: TzarRuntime):
        raise NotImplementedError
