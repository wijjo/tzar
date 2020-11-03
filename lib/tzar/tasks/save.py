"""Tzar save command."""

import jiig

from tzar.internal.task_runner import TzarTaskRunner

from .arguments import ArchiveFolderArg, SourceNameArg, MethodArg, TagsArg, SourceFolderArg


@jiig.task(
    'save',
    jiig.Arg('EXCLUDE',
             jiig.arg.String,
             description='Exclusion pattern(s), including gitignore-style wildcards',
             cardinality='*',
             flags=['-e', '--exclude']),
    jiig.Arg('PROGRESS',
             jiig.arg.Boolean,
             description='Display progress statistics',
             flags=['-p', '--progress']),
    jiig.Arg('DISABLE_TIMESTAMP',
             jiig.arg.Boolean,
             description=f'Disable adding timestamp to name',
             flags=['-T', '--no-timestamp']),
    jiig.Arg('GITIGNORE',
             jiig.arg.Boolean,
             description='Use .gitignore exclusions',
             flags='--gitignore'),
    jiig.Arg('KEEP_LIST',
             jiig.arg.Boolean,
             description='Do not delete temporary file list when done',
             flags='--keep-list'),
    jiig.Arg('PENDING',
             jiig.arg.Boolean,
             description='Save only modified version-controlled files',
             flags='--pending'),
    ArchiveFolderArg(),
    SourceNameArg(),
    MethodArg(),
    TagsArg(),
    SourceFolderArg(cardinality='?'),
    description='Save an archive of the working folder or another folder',
)
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
