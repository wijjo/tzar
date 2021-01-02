"""Tzar prune command."""

from typing import Text, List

import jiig


class TaskClass(jiig.Task):
    """Delete archive(s) [destructive]."""

    # For type inspection only.
    class Data:
        ARCHIVE_PATH: List[Text]
    data: Data

    args = {
        'ARCHIVE_PATH[+]': ('Path(s) to source archive file or folder',
                            jiig.path.check_exists),
    }

    def on_run(self):
        pass
