"""Tzar save command."""

import jiig

from tzar import arguments
from tzar.runtime import TzarRuntime


@jiig.task
def save(
    runtime: TzarRuntime,
    exclude: arguments.exclude_option,
    progress: arguments.progress_option,
    disable_timestamp: arguments.disable_timestamp_option,
    gitignore: arguments.gitignore_option,
    keep_list: arguments.keep_list_option,
    pending: arguments.pending_option,
    tags: arguments.tags_option,
    archive_folder: arguments.archive_folder_option,
    source_name: arguments.source_name_option,
    source_folder: arguments.source_folder_option,
    method: arguments.method_option,
):
    """Save an archive of the working folder or another folder."""
    runtime.save_archive(source_folder,
                         archive_folder,
                         method,
                         source_name=source_name,
                         gitignore=gitignore,
                         excludes=exclude,
                         pending=pending,
                         timestamp=not disable_timestamp,
                         progress=progress,
                         keep_list=keep_list,
                         tags=tags)
