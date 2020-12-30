"""Tzar save command."""

from jiig import BoolOpt, Opt

from tzar.internal.tzar_task import TzarTask

from . import arguments


class TaskClass(TzarTask):
    """Save an archive of the working folder or another folder."""

    opts = [
        Opt(('-e', '--exclude'), 'EXCLUDE',
            'Exclusion pattern(s), including gitignore-style wildcards',
            cardinality='*'),
        BoolOpt(('-p', '--progress'), 'PROGRESS',
                'Display progress statistics'),
        BoolOpt(('-T', '--no-timestamp'), 'DISABLE_TIMESTAMP',
                'Disable adding timestamp to name'),
        BoolOpt('--gitignore', 'GITIGNORE',
                'Use .gitignore exclusions'),
        BoolOpt('--keep-list', 'KEEP_LIST',
                'Do not delete temporary file list when done'),
        BoolOpt('--pending', 'PENDING',
                'Save only modified version-controlled files'),
        arguments.archive_folder_option(),
        arguments.source_name_option(),
        arguments.method_option(),
        arguments.tags_option(),
        arguments.source_folder_option(cardinality='?'),
    ]

    def on_run(self):
        archiver = self.create_archiver()
        archiver.save_archive(self.data.METHOD,
                              gitignore=self.data.GITIGNORE,
                              excludes=self.data.EXCLUDE,
                              pending=self.data.PENDING,
                              timestamp=not self.data.DISABLE_TIMESTAMP,
                              progress=self.data.PROGRESS,
                              keep_list=self.data.KEEP_LIST,
                              tags=self.data.TAGS)
