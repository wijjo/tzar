"""
Tzar prune command.

Pruning options provide flexibility for specifying different algorithms for
choosing which archives to purge.

Due to the destructive nature of these actions, an action summary is displayed,
followed by a confirmation prompt. A NO_CONFIRMATION option can disable the
confirmation prompt, e.g. for automation scripts.
"""

from jiig import task
from tzar.internal.task_runner import TzarTaskRunner
from .arguments import age_max_argument, age_min_argument, archive_folder_argument, \
    date_max_argument, date_min_argument, interval_max_argument, interval_min_argument, \
    no_confirmation_argument, source_name_argument, source_folder_argument, tags_argument


@task('prune',
      age_max_argument(),
      age_min_argument(),
      archive_folder_argument(),
      date_max_argument(),
      date_min_argument(),
      interval_max_argument(),
      interval_min_argument(),
      no_confirmation_argument(),
      source_name_argument(),
      source_folder_argument(),
      tags_argument(),
      description='Prune archives to save space [destructive]')
def task_prune(runner: TzarTaskRunner):
    for item in runner.list_catalog():
        print('-->', item.time_string)
