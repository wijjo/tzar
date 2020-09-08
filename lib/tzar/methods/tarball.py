"""Tarball archive utilities."""

from typing import List, Text, Any

from jiig.utility.filesystem import choose_program_alternative

from .base import MethodData


def build_tarball_save_command(method_data: MethodData,
                               *compressors: Any
                               ) -> List[Text]:
    """
    Build command arguments for saving tarball with optional compression+progress.

    :param method_data: specification data for tarball archive
    :param compressors: compression programs, with optional arguments when it's a sequence
    :return:
    """
    cmd_args = ['tar', f'cf', '-', '-T', method_data.source_list_path]
    if method_data.verbose:
        cmd_args.append('-v')
    if method_data.pv_progress:
        # Create a pipeline with "pv" for progress reporting.
        cmd_args.extend(['|', 'pv', '-s', method_data.total_bytes, '-ptebar'])
    # choose_program_alternative() returns a command argument list.
    if compressors:
        cmd_args.extend(['|'] + choose_program_alternative(*compressors, required=True))
    cmd_args.extend(['>', method_data.target_path])
    return cmd_args
