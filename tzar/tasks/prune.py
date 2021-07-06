"""
Tzar prune command.

Pruning options provide flexibility for specifying different algorithms for
choosing which archives to purge.

Due to the destructive nature of these actions, an action summary is displayed,
followed by a confirmation prompt. A NO_CONFIRMATION option can disable the
confirmation prompt, e.g. for automation scripts.
"""

import jiig

from tzar import arguments
from tzar.runtime import TzarRuntime


# noinspection PyUnusedLocal
@jiig.task
def prune(
    runtime: TzarRuntime,
    age_max: arguments.age_max_option,
    age_min: arguments.age_min_option,
    date_max: arguments.date_max_option,
    date_min: arguments.date_min_option,
    interval_max: arguments.interval_max_option,
    interval_min: arguments.interval_min_option,
    tags: arguments.tags_option,
    no_confirmation: arguments.no_confirmation_option,
    archive_folder: arguments.archive_folder_option,
    source_name: arguments.source_name_option,
    source_folder: arguments.source_folder_option,
):
    """Prune archives to save space. [^destructive]"""
    for item in runtime.list_catalog(
            source_folder,
            archive_folder,
            source_name=source_name,
            date_min=date_min,
            date_max=date_max,
            age_min=age_min,
            age_max=age_max,
            interval_min=interval_min,
            interval_max=interval_max,
            tags=tags):
        print(f'--> {item.time_string}')
