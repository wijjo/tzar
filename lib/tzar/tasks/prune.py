"""
Tzar prune command.

Pruning options provide flexibility for specifying different algorithms for
choosing which archives to purge.

Due to the destructive nature of these actions, an action summary is displayed,
followed by a confirmation prompt. A NO_CONFIRMATION option can disable the
confirmation prompt, e.g. for automation scripts.
"""

import jiig

from tzar.internal.tzar_task_runner import TzarTaskRunner

from . import arguments


@jiig.task('prune',
           arguments.age_max_option(),
           arguments.age_min_option(),
           arguments.archive_folder_option(),
           arguments.date_max_option(),
           arguments.date_min_option(),
           arguments.interval_max_option(),
           arguments.interval_min_option(),
           arguments.no_confirmation_option(),
           arguments.source_name_option(),
           arguments.source_folder_option(),
           arguments.tags_option(),
           description='Prune archives to save space [destructive]')
def task_prune(runner: TzarTaskRunner):
    for item in runner.list_catalog():
        print('-->', item.time_string)
