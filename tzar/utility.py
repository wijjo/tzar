"""Tzar utility functions."""

from typing import Text, Optional

from jiig.util.log import log_error
from jiig.util.general import format_human_byte_count


def format_file_size(byte_count: Optional[int],
                     decimal_places: int = 1,
                     size_unit_binary: bool = False,
                     size_unit_decimal: bool = False,
                     default: Text = None
                     ) -> Text:
    """
    Format size with support for common size formatting options.

    Note that decimal_units and binary_units should not both be True. If both
    are False the number is converted to text without additional formatting.

    :param byte_count: size as byte count to convert to text
    :param decimal_places: number of decimal places to display
    :param size_unit_binary: format binary 1024-based KiB/MiB size
    :param size_unit_decimal: format binary 1000-based KB/MB size
    :param default: text returned when byte_count is None (default is '-')
    :return: formatted byte count string, with units applied as needed
    """
    if byte_count is None:
        return default or '-'
    if size_unit_binary:
        unit_format = 'b'
        if size_unit_decimal:
            log_error('Ignoring decimal units option when binary units are selected.',
                      issue_once_tag='REDUNDANT_UNIT_OPTIONS')
    elif size_unit_decimal:
        unit_format = 'd'
    else:
        unit_format = None
    return format_human_byte_count(byte_count,
                                   unit_format=unit_format,
                                   decimal_places=decimal_places)
