"""Tzar save command."""

import jiig

from tzar import arguments
from tzar.runtime import TzarRuntime


class Task(jiig.Task):
    """Save an archive of the working folder or another folder."""

    exclude: arguments.exclude_option
    progress: arguments.progress_option
    disable_timestamp: arguments.disable_timestamp_option
    gitignore: arguments.gitignore_option
    keep_list: arguments.keep_list_option
    pending: arguments.pending_option
    tags: arguments.tags_option
    archive_folder: arguments.archive_folder_option
    source_name: arguments.source_name_option
    source_folder: arguments.source_folder_option
    method: arguments.method_option

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
