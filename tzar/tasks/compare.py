"""Tzar compare command."""

import jiig


class Task(jiig.Task):
    """Compare archive to existing files."""

    archive_path: jiig.filesystem_object(
        'Path to source archive file or folder.',
        exists=True)

    source_folder: jiig.filesystem_folder(
        'Source folder.',
        absolute_path=True,
        cli_flags=('-s', '--source-folder')
    ) = '.'

    def on_run(self, _runtime: jiig.Runtime):
        raise NotImplementedError
