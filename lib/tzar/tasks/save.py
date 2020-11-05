"""Tzar save command."""

from jiig import task, argument
from jiig.arg import boolean, text
from tzar.internal.task_runner import TzarTaskRunner

from .arguments import archive_folder_argument, source_name_argument, method_argument, \
    tags_argument, source_folder_argument


@task('save',
      argument('EXCLUDE',
               text,
               description='Exclusion pattern(s), including gitignore-style wildcards',
               cardinality='*',
               flags=['-e', '--exclude']),
      argument('PROGRESS',
               boolean,
               description='Display progress statistics',
               flags=['-p', '--progress']),
      argument('DISABLE_TIMESTAMP',
               boolean,
               description=f'Disable adding timestamp to name',
               flags=['-T', '--no-timestamp']),
      argument('GITIGNORE',
               boolean,
               description='Use .gitignore exclusions',
               flags='--gitignore'),
      argument('KEEP_LIST',
               boolean,
               description='Do not delete temporary file list when done',
               flags='--keep-list'),
      argument('PENDING',
               boolean,
               description='Save only modified version-controlled files',
               flags='--pending'),
      archive_folder_argument(),
      source_name_argument(),
      method_argument(),
      tags_argument(),
      source_folder_argument(cardinality='?'),
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
