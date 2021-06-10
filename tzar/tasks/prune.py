"""
Tzar prune command.

Pruning options provide flexibility for specifying different algorithms for
choosing which archives to purge.

Due to the destructive nature of these actions, an action summary is displayed,
followed by a confirmation prompt. A NO_CONFIRMATION option can disable the
confirmation prompt, e.g. for automation scripts.
"""

import os

import jiig

from tzar.internal.constants import DEFAULT_ARCHIVE_FOLDER
from tzar.internal.archiver import create_archiver


class Task(jiig.Task):
    """Prune archives to save space [destructive]."""

    age_max: jiig.age(
        'Maximum archive age [age_option].',
        cli_flags='--age-max')

    age_min: jiig.age(
        'Minimum archive age [age_option].',
        cli_flags='--age-min')

    date_max: jiig.timestamp(
        'Maximum (latest) archive date.',
        cli_flags='--date-max')

    date_min: jiig.timestamp(
        'Minimum (earliest) archive date.',
        cli_flags='--date-min')

    interval_max: jiig.interval(
        'Maximum interval (n[HMS]) between saves to consider.',
        cli_flags='--interval-max')

    interval_min: jiig.interval(
        'Minimum interval (n[HMS]) between saves to consider.',
        cli_flags='--interval-min')

    no_confirmation: jiig.boolean(
        'Execute destructive actions without prompting for confirmation.',
        cli_flags='--no-confirmation')

    tags: jiig.comma_tuple(
        'Comma-separated archive tags.',
        cli_flags=('-t', '--tags'))

    archive_folder: jiig.filesystem_folder(
        'Archive folder.',
        cli_flags=('-f', '--archive-folder')
    ) = DEFAULT_ARCHIVE_FOLDER

    source_name: jiig.text(
        'Source name.',
        cli_flags=('-n', '--name')
    ) = os.path.basename(os.getcwd())

    source_folder: jiig.filesystem_folder(
        'Source folder.',
        absolute_path=True,
        cli_flags=('-s', '--source-folder')
    ) = '.'

    def on_run(self, runtime: jiig.Runtime):
        archiver = create_archiver(self.source_folder,
                                   self.archive_folder,
                                   source_name=self.source_name,
                                   verbose=runtime.options.verbose,
                                   dry_run=runtime.options.dry_run)
        for item in archiver.list_catalog(
                date_min=self.date_min,
                date_max=self.date_max,
                age_min=self.age_min,
                age_max=self.age_max,
                interval_min=self.interval_min,
                interval_max=self.interval_max,
                tags=self.tags):
            print('-->', item.time_string)
