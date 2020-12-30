"""Tzar-specific extended Jiig Task class."""

import os
from typing import Text, Optional, List, Callable

import jiig

from jiig.utility.console import log_error
from jiig.utility.general import format_human_byte_count

from .archiver import Archiver, create_archiver, CatalogItem
from .constants import DEFAULT_ARCHIVE_FOLDER


class TzarTask(jiig.Task):
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
        if self.data.SIZE_UNIT_BINARY:
            unit_format = 'b'
            if self.data.SIZE_UNIT_DECIMAL:
                log_error('Ignoring decimal units option when binary units are selected.',
                          issue_once_tag='REDUNDANT_UNIT_OPTIONS')
        elif self.data.SIZE_UNIT_DECIMAL:
            unit_format = 'd'
        else:
            unit_format = None
        return format_human_byte_count(byte_count,
                                       unit_format=unit_format,
                                       decimal_places=decimal_places)

    def _get_date_age_timestamp(self,
                                date_name: Text,
                                age_name: Text,
                                choice_function: Callable[[float, float], float],
                                ) -> Optional[float]:
        date_timestamp: Optional[float] = getattr(self.data, date_name, None)
        age_timestamp: Optional[float] = getattr(self.data, age_name, None)
        if date_timestamp is None:
            if age_timestamp is None:
                return None
            return age_timestamp
        if age_timestamp is None:
            return date_timestamp
        return choice_function(date_timestamp, age_timestamp)

    @property
    def source_name(self) -> Optional[Text]:
        """
        Get source name from options, if available.

        :return: source name or None
        """
        return (getattr(self.data, 'SOURCE_NAME', None)
                or os.path.basename(self.source_folder))

    @property
    def source_folder(self) -> Optional[Text]:
        """
        Get source folder from options, if available.

        :return: source folder or None
        """
        value = getattr(self.data, 'SOURCE_FOLDER', None)
        if value is not None and not isinstance(value, str):
            raise ValueError(f'SOURCE_FOLDER {value} is not a single string value.')
        return value or os.getcwd()

    @property
    def archive_folder(self) -> Optional[Text]:
        """
        Get archive folder from options, if available.

        :return: archive folder or None
        """
        return (getattr(self.data, 'ARCHIVE_FOLDER', None)
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

    def create_archiver(self) -> Archiver:
        """
        Pass-through to archiver.create_archiver() that uses standard Tzar options.

        Applies verbose and dry_run options.

        :return: archiver object
        """
        return create_archiver(self.source_name,
                               self.source_folder,
                               self.archive_folder,
                               verbose=self.params.VERBOSE,
                               dry_run=self.params.DRY_RUN)

    def list_catalog(self) -> List[CatalogItem]:
        """
        Create an archiver and list the catalog using relevant Tzar options.

        :return: catalog item list
        """
        return self.create_archiver().list_catalog(
            timestamp_min=self.timestamp_min,
            timestamp_max=self.timestamp_max,
            interval_min=getattr(self.data, 'INTERVAL_MIN', None),
            interval_max=getattr(self.data, 'INTERVAL_MAX', None),
            tags=self.data.TAGS)

    def on_run(self):
        """Required call-back hook."""
        raise NotImplementedError
