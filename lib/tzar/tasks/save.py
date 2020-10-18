"""Tzar save command."""

from jiig import task

from tzar import TzarTaskRunner


@task(
    'save',
    help='save an archive of the working folder',
    arguments=[
        (['-e', '--exclude'],
         {'dest': 'EXCLUDE',
          'nargs': '*',
          'help': 'exclusion pattern(s), including gitignore-style wildcards'}),
        (['-p', '--progress'],
         {'dest': 'PROGRESS',
          'action': 'store_true',
          'help': 'display progress statistics'}),
        (['-T', '--no-timestamp'],
         {'dest': 'DISABLE_TIMESTAMP',
          'action': 'store_true',
          'help': f'disable adding timestamp to name'}),
        ('--gitignore',
         {'dest': 'GITIGNORE',
          'action': 'store_true',
          'help': 'use .gitignore exclusions'}),
        ('--keep-list',
         {'dest': 'KEEP_LIST',
          'action': 'store_true',
          'help': 'do not delete temporary file list when done'}),
        ('--pending',
         {'dest': 'PENDING',
          'action': 'store_true',
          'help': 'save only modified version-controlled files'}),
        (['-f', '--archive-folder'],
         'ARCHIVE_FOLDER'),
        (['-n', '--name'],
         'SOURCE_NAME'),
        (['-m', '--method'],
         'METHOD'),
        (['-t', '--tags'],
         'TAGS'),
        'SOURCE_FOLDER?'
    ],
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
