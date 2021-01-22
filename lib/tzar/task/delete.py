"""Tzar prune command."""

from typing import Text, List

from jiig import arg, model


class TaskClass(model.Task):
    """Delete archive(s) [destructive]."""

    # For type inspection only.
    class Data:
        ARCHIVE_PATH: List[Text]
    data: Data

    args = {
        'ARCHIVE_PATH[+]': ('Path(s) to source archive file or folder',
                            arg.path_exists),
    }

    def on_run(self):
        pass
