"""Tzar save command."""

import os

import jiig

from tzar import constants
from tzar.runtime import TzarRuntime


@jiig.task(
    cli={
        'options': {
            'exclude': constants.OPTION_EXCLUDE,
            'progress': constants.OPTION_PROGRESS,
            'disable_timestamp': constants.OPTION_DISABLE_TIMESTAMP,
            'gitignore': constants.OPTION_GITIGNORE,
            'keep_list': constants.OPTION_KEEP_LIST,
            'pending': constants.OPTION_PENDING,
            'tags': constants.OPTION_TAGS,
            'archive_folder': constants.OPTION_ARCHIVE_FOLDER,
            'source_name': constants.OPTION_SOURCE_NAME,
            'source_folder': constants.OPTION_SOURCE_FOLDER,
            'method': constants.OPTION_METHOD,
        }
    }
)
def save(
    runtime: TzarRuntime,
    exclude: jiig.f.text(repeat=(None, None)),
    progress: jiig.f.boolean(),
    disable_timestamp: jiig.f.boolean(),
    gitignore: jiig.f.boolean(),
    keep_list: jiig.f.boolean(),
    pending: jiig.f.boolean(),
    tags: jiig.f.comma_tuple(),
    archive_folder: jiig.f.filesystem_folder(absolute_path=True) = constants.DEFAULT_ARCHIVE_FOLDER,
    source_name: jiig.f.text() = os.path.basename(os.getcwd()),
    source_folder: jiig.f.filesystem_folder(absolute_path=True) = '.',
    method: jiig.f.text(choices=TzarRuntime.get_method_names()) = constants.DEFAULT_METHOD,
):
    """
    Save an archive of the working folder or another folder.

    :param runtime: Jiig runtime API.
    :param exclude: Exclusion pattern(s), including gitignore-style wildcards.
    :param progress: Display progress statistics.
    :param disable_timestamp: Disable adding timestamp to name.
    :param gitignore: Use .gitignore exclusions.
    :param keep_list: Do not delete temporary file list when done.
    :param pending: Save only modified version-controlled files.
    :param tags: Comma-separated archive tags.
    :param archive_folder: Archive folder.
    :param source_name: Source name.
    :param source_folder: Source folder.
    :param method: Archive method.
    """
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
