"""Tzar delete command."""

import jiig

from tzar.runtime import TzarRuntime


# noinspection PyUnusedLocal
@jiig.task()
def delete(
    runtime: TzarRuntime,
    archive_paths: jiig.f.filesystem_object(exists=True, repeat=(1, None)),
):
    """
    Delete archive(s). [^destructive]

    :param runtime: Jiig runtime API.
    :param archive_paths: Path(s) to source archive file or folder.
    """
    raise NotImplementedError
