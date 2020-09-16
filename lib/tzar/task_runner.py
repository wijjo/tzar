"""Tzar-specific task runner."""

from typing import Text, Optional

from jiig import runner_factory, TaskRunner, RunnerData
from jiig.utility.console import log_error
from jiig.utility.general import format_byte_count

from tzar import archiver


class TzarTaskRunner(TaskRunner):
    """Tzar-specific task runner."""

    def format_size(self,
                    byte_count: Optional[int],
                    decimal_places: int = 1,
                    default: Text = None
                    ) -> Text:
        """
        Format size with support for common size formatting options.

        Note that decimal_units and binary_units should not both be True. If both
        are False the number is converted to text without additional formatting.

        :param byte_count: size as byte count to convert to text
        :param decimal_places: number of decimal places to display
        :param default: text returned when byte_count is None (default is '-')
        :return: formatted byte count string, with units applied as needed
        """
        if byte_count is None:
            return default or '-'
        if self.args.BINARY_SIZE_UNIT:
            unit_format = 'b'
            if self.args.DECIMAL_SIZE_UNIT:
                log_error('Ignoring decimal units option when binary units are selected.',
                          issue_once_tag='REDUNDANT_UNIT_OPTIONS')
        elif self.args.DECIMAL_SIZE_UNIT:
            unit_format = 'd'
        else:
            unit_format = None
        return format_byte_count(byte_count,
                                 unit_format=unit_format,
                                 decimal_places=decimal_places)

    def create_archiver(self,
                        source_name: Text = None,
                        archive_folder: Text = None,
                        labels: Text = None
                        ) -> archiver.Archiver:
        return archiver.create_archiver(source_name=source_name,
                                        archive_folder=archive_folder,
                                        labels=labels,
                                        verbose=self.verbose,
                                        dry_run=self.dry_run)


@runner_factory()
def create_runner(data: RunnerData) -> TaskRunner:
    """
    Substitute Tzar-customized TaskRunner subclass.

    :return: TaskRunner instance
    """
    return TzarTaskRunner(data)
