"""Support for Zip archives."""

from tzar.archiver import archive_method

from .base import MethodData, ArchiveMethodBase, MethodSaveData


@archive_method('zip')
class ArchiveMethodZip(ArchiveMethodBase):
    def handle_save(self, method_data: MethodData) -> MethodSaveData:
        cmd_args = ['zip', '-r', '-', '.', f'-i@{method_data.source_list_path}']
        if not method_data.verbose:
            cmd_args.append('-q')
        if method_data.pv_progress:
            cmd_args.extend(['|', 'pv', '-bret'])
        zip_path = method_data.target_path + '.zip'
        cmd_args.extend(['>', zip_path])
        return MethodSaveData(target_path=zip_path, command_arguments=cmd_args)
