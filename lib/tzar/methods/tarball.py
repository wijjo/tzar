"""Tarball archive utilities."""

import tarfile
from typing import List, Text, Union, Sequence

from jiig.utility.filesystem import choose_program_alternative
from jiig.utility.general import make_list

from .base import MethodSaveData, MethodSaveResult, MethodListItem


def handle_tarball_save(save_data: MethodSaveData,
                        compressors: Union[List[Text], Text] = None,
                        extension: Text = None,
                        ) -> MethodSaveResult:
    """
    Build command arguments for saving tarball with optional compression+progress.

    :param save_data: specification data for saving tarball archive
    :param extension: optional extension without leading '.' appended to ".tar"
    :param compressors: compression programs, with optional arguments when it's a sequence
    :return:
    """
    cmd_args = ['tar', f'cf', '-', '-T', save_data.source_list_path]
    if save_data.verbose:
        cmd_args.append('-v')
    # choose_program_alternative() returns a command argument list.
    if compressors:
        compression_program = choose_program_alternative(
            *make_list(compressors, strings=True),
            required=True)
        cmd_args.extend(['|'] + compression_program)
    if save_data.pv_progress:
        # Create a pipeline with "pv" for progress reporting.
        cmd_args.extend(['|', 'pv', '-bret'])
    archive_path_parts = [save_data.archive_path, 'tar']
    if extension:
        archive_path_parts.append(extension)
    archive_path = '.'.join(archive_path_parts)
    cmd_args.extend(['>', archive_path])
    return MethodSaveResult(archive_path=archive_path, command_arguments=cmd_args)


def handle_tarball_list(archive_path: Text,
                        compression: Text = None
                        ) -> Sequence[MethodListItem]:
    """
    Implementation to list tarball contents.

    :param archive_path: archive tarball file path
    :param compression: optional compression specification, e.g. 'gz'
    :return: sequence of archive items
    """
    mode = f'r:{compression}' if compression else 'r'
    with tarfile.open(archive_path, mode=mode) as tar_file:
        for info in tar_file.getmembers():
            file_size = info.size if not info.isdir() else None
            yield MethodListItem(path=info.name, time=info.mtime, size=file_size)


def handle_tarball_get_name(archive_name: Text,
                            extension: Text = None,
                            ) -> Text:
    """
    Implementation to preprocess archive name for further parsing.

    :param archive_name: archive file name
    :param extension: optional extension without leading '.' appended to ".tar"
    :return: stripped name suitable for further parsing
    """
    full_extension = f'.tar.{extension}'
    if archive_name.endswith(full_extension):
        return archive_name[:-len(full_extension)]
    return archive_name
