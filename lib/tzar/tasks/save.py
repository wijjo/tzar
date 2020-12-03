"""Tzar save command."""

import jiig

from tzar.internal.tzar_task_runner import TzarTaskRunner

from . import arguments


@jiig.task('save',
           jiig.option('EXCLUDE',
                       ('-e', '--exclude'),
                       description='Exclusion pattern(s), including gitignore-style wildcards',
                       cardinality='*'),
           jiig.bool_option('PROGRESS',
                            ('-p', '--progress'),
                            description='Display progress statistics'),
           jiig.bool_option('DISABLE_TIMESTAMP',
                            ('-T', '--no-timestamp'),
                            description=f'Disable adding timestamp to name'),
           jiig.bool_option('GITIGNORE',
                            '--gitignore',
                            description='Use .gitignore exclusions'),
           jiig.bool_option('KEEP_LIST',
                            '--keep-list',
                            description='Do not delete temporary file list when done'),
           jiig.bool_option('PENDING',
                            '--pending',
                            description='Save only modified version-controlled files'),
           arguments.archive_folder_option(),
           arguments.source_name_option(),
           arguments.method_option(),
           arguments.tags_option(),
           arguments.source_folder_option(cardinality='?'),
           description='Save an archive of the working folder or another folder')
def task_save(runner: TzarTaskRunner):
    archiver = runner.create_archiver()
    archiver.save_archive(runner.args.METHOD,
                          gitignore=runner.args.GITIGNORE,
                          excludes=runner.args.EXCLUDE,
                          pending=runner.args.PENDING,
                          timestamp=not runner.args.DISABLE_TIMESTAMP,
                          progress=runner.args.PROGRESS,
                          keep_list=runner.args.KEEP_LIST,
                          tags=runner.args.TAGS)
