"""Tzar-specific task runner."""

import os
from time import mktime
from typing import Text, Optional, Tuple, List, Callable

from jiig import runner_factory, TaskRunner, RunnerData
from jiig.utility.console import log_error
from jiig.utility.date_time import parse_date_time, apply_date_time_delta_string, parse_time_interval
from jiig.utility.general import format_byte_count

from tzar import archiver, CatalogItem
from tzar.constants import DEFAULT_ARCHIVE_FOLDER


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
        if self.args.SIZE_UNIT_BINARY:
            unit_format = 'b'
            if self.args.SIZE_UNIT_DECIMAL:
                log_error('Ignoring decimal units option when binary units are selected.',
                          issue_once_tag='REDUNDANT_UNIT_OPTIONS')
        elif self.args.SIZE_UNIT_DECIMAL:
            unit_format = 'd'
        else:
            unit_format = None
        return format_byte_count(byte_count,
                                 unit_format=unit_format,
                                 decimal_places=decimal_places)

    def _get_date_age_timestamp(self,
                                date_name: Text,
                                age_name: Text,
                                choice_function: Callable[[float, float], float],
                                ) -> Optional[float]:
        timestamp_result: Optional[float] = None
        if date_name in self.args:
            parsed_time_struct = parse_date_time(getattr(self.args, date_name))
            if parsed_time_struct:
                timestamp_result = mktime(parsed_time_struct)
        if age_name in self.args:
            age_string = getattr(self.args, age_name)
            if age_string:
                age_time_struct = apply_date_time_delta_string(age_string, negative=True)
                if age_time_struct:
                    age_timestamp = mktime(age_time_struct)
                    if timestamp_result is None:
                        timestamp_result = age_timestamp
                    else:
                        timestamp_result = choice_function(timestamp_result, age_timestamp)
        return timestamp_result

    @property
    def source_name(self) -> Optional[Text]:
        """
        Get source name from options, if available.

        :return: source name or None
        """
        return (getattr(self.args, 'SOURCE_NAME', None)
                or os.path.basename(self.source_folder))

    @property
    def source_folder(self) -> Optional[Text]:
        """
        Get source folder from options, if available.

        :return: source folder or None
        """
        value = getattr(self.args, 'SOURCE_FOLDER', None)
        if value is not None and not isinstance(value, str):
            raise ValueError(f'SOURCE_FOLDER {value} is not a single string value.')
        return value or os.getcwd()

    @property
    def archive_folder(self) -> Optional[Text]:
        """
        Get archive folder from options, if available.

        :return: archive folder or None
        """
        return (getattr(self.args, 'ARCHIVE_FOLDER', None)
                or DEFAULT_ARCHIVE_FOLDER)

    @property
    def timestamp_min(self) -> Optional[float]:
        """
        Determine minimum (earliest) time stamp based on DATE_MIN/AGE_MAX args.

        :return: timestamp or None if information is bad or not available
        """
        return self._get_date_age_timestamp('DATE_MIN', 'AGE_MAX', max)

    @property
    def timestamp_max(self) -> Optional[float]:
        """
        Determine maximum (latest) time stamp based on DATE_MAX/AGE_MIN args.

        :return: timestamp or None if information is bad or not available
        """
        return self._get_date_age_timestamp('DATE_MAX', 'AGE_MIN', min)

    @property
    def interval_min(self) -> Optional[float]:
        """
        Convert an INTERVAL_MIN arg value to float seconds, if available.

        :return: minimum interval seconds or None
        """
        return parse_time_interval(self.args.INTERVAL_MIN)

    @property
    def interval_max(self) -> Optional[float]:
        """
        Convert an INTERVAL_MAX arg value to float seconds, if available.

        :return: maximum interval seconds or None
        """
        return parse_time_interval(self.args.INTERVAL_MAX)

    @property
    def tags(self) -> Optional[Tuple[Text]]:
        tag_tuple: Optional[Tuple[Text]] = None
        if 'TAGS' in self.args:
            tag_string = self.args.TAGS
            if tag_string is not None:
                tag_list: List[Text] = [tag.strip() for tag in tag_string.split(',')]
                tag_tuple = tuple(tag_list)
        return tag_tuple

    def create_archiver(self) -> archiver.Archiver:
        """
        Pass-through to archiver.create_archiver() that uses standard Tzar options.

        Applies verbose and dry_run options.

        :return: archiver object
        """
        return archiver.create_archiver(self.source_name,
                                        self.source_folder,
                                        self.archive_folder,
                                        verbose=self.verbose,
                                        dry_run=self.dry_run)

    def list_catalog(self) -> List[CatalogItem]:
        """
        Create an archiver and list the catalog using relevant Tzar options.

        :return: catalog item list
        """
        return self.create_archiver().list_catalog(
            timestamp_min=self.timestamp_min,
            timestamp_max=self.timestamp_max,
            interval_min=self.interval_min,
            interval_max=self.interval_max,
            tags=self.tags)


@runner_factory()
def create_runner(data: RunnerData) -> TaskRunner:
    """
    Substitute Tzar-customized TaskRunner subclass.

    :return: TaskRunner instance
    """
    return TzarTaskRunner(data)
