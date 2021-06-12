"""Tzar save command."""

import os

import jiig

from tzar.constants import DEFAULT_ARCHIVE_FOLDER
from tzar.method import DEFAULT_METHOD
from tzar.runtime import TzarRuntime


class Task(jiig.Task):
    """Save an archive of the working folder or another folder."""

    exclude: jiig.text(
        'Exclusion pattern(s), including gitignore-style wildcards.',
        repeat=None,
        cli_flags=('-e', '--exclude'))

    progress: jiig.boolean(
        'Display progress statistics.',
        cli_flags=('-p', '--progress'))

    disable_timestamp: jiig.boolean(
        'Disable adding timestamp to name.',
        cli_flags=('-T', '--no-timestamp'))

    gitignore: jiig.boolean(
        'Use .gitignore exclusions.',
        cli_flags='--gitignore')

    keep_list: jiig.boolean(
        'Do not delete temporary file list when done.',
        cli_flags='--keep-list')

    pending: jiig.boolean(
        'Save only modified version-controlled files.',
        cli_flags='--pending')

    tags: jiig.comma_tuple(
        'Comma-separated archive tags.',
        cli_flags=('-t', '--tags'))

    archive_folder: jiig.filesystem_folder(
        'Archive folder.',
        cli_flags=('-f', '--archive-folder')
    ) = DEFAULT_ARCHIVE_FOLDER

    source_name: jiig.text(
        'Source name.',
        cli_flags=('-n', '--name')
    ) = os.path.basename(os.getcwd())

    method: jiig.text(
        'Archive method.',
        cli_flags=('-m', '--method'),
        choices=TzarRuntime.get_method_names(),
    ) = DEFAULT_METHOD

    source_folder: jiig.filesystem_folder(
        'Source folder.',
        absolute_path=True,
        cli_flags=('-s', '--source-folder')
    ) = '.'

    def on_run(self, runtime: TzarRuntime):
        runtime.save_archive(self.source_folder,
                             self.archive_folder,
                             self.method,
                             source_name=self.source_name,
                             gitignore=self.gitignore,
                             excludes=self.exclude,
                             pending=self.pending,
                             timestamp=not self.disable_timestamp,
                             progress=self.progress,
                             keep_list=self.keep_list,
                             tags=self.tags)
