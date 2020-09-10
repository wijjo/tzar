"""Tarball archive utilities."""

from typing import List, Text, Union

from jiig.utility.filesystem import choose_program_alternative
from jiig.utility.general import make_list

from .base import MethodData, MethodSaveData


def handle_tarball_save(method_data: MethodData,
                        compressors: Union[List[Text], Text] = None,
                        extension: Text = None,
                        ) -> MethodSaveData:
    """
    Build command arguments for saving tarball with optional compression+progress.

    :param method_data: specification data for tarball archive
    :param extension: optional extension without leading '.' appended to ".tar"
    :param compressors: compression programs, with optional arguments when it's a sequence
    :return:
    """
    cmd_args = ['tar', f'cf', '-', '-T', method_data.source_list_path]
    if method_data.verbose:
        cmd_args.append('-v')
    # choose_program_alternative() returns a command argument list.
    if compressors:
        compression_program = choose_program_alternative(
            *make_list(compressors, strings=True),
            required=True)
        cmd_args.extend(['|'] + compression_program)
    if method_data.pv_progress:
        # Create a pipeline with "pv" for progress reporting.
        cmd_args.extend(['|', 'pv', '-bret'])
    target_path_parts = [method_data.target_path, 'tar']
    if extension:
        target_path_parts.append(extension)
    target_path = '.'.join(target_path_parts)
    cmd_args.extend(['>', target_path])
    return MethodSaveData(target_path=target_path, command_arguments=cmd_args)
