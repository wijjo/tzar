# Copyright (C) 2021-2022, Steven Cooper
#
# This file is part of Tzar.
#
# Tzar is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Tzar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Tzar.  If not, see <https://www.gnu.org/licenses/>.

"""Discovered archive file."""

import os
from dataclasses import dataclass
from time import mktime
from typing import Text, Type, List, Optional

from .archive_method import ArchiveMethodBase, RegisteredMethod
from .constants import TIMESTAMP_REGEX
from .methods import METHOD_MAP


@dataclass
class ArchiveNameData:
    source_name: Text
    time_stamp: Optional[float]
    tags: List[Text]


@dataclass
class DiscoveredArchive:
    path: Text
    file_time: float
    file_size: int
    method_name: Text
    method_cls: Type[ArchiveMethodBase]
    _archive_name_data: Optional[ArchiveNameData] = None

    @property
    def file_name(self) -> Text:
        return os.path.basename(self.path)

    @property
    def archive_name(self) -> Text:
        return self.method_cls.handle_get_name(self.file_name)

    @property
    def archive_name_data(self) -> ArchiveNameData:
        if self._archive_name_data is None:
            name_parts = self.archive_name.split('_')
            source_name = name_parts[0]
            # Parse name to extract date, time, and tags.
            tags: List[Text] = []
            time_stamp: Optional[float] = None
            if len(name_parts) >= 2:
                timestamp_matched = TIMESTAMP_REGEX.match(name_parts[1])
                if timestamp_matched:
                    time_stamp = mktime((
                        int(timestamp_matched.group('year')),
                        int(timestamp_matched.group('month')),
                        int(timestamp_matched.group('day')),
                        int(timestamp_matched.group('hours')),
                        int(timestamp_matched.group('minutes')),
                        int(timestamp_matched.group('seconds')),
                        0, 0, -1))
                    # Handles both comma and underscore-separated tags.
                    raw_tags = ','.join(name_parts[2:])
                else:
                    raw_tags = ','.join(name_parts[1:])
                tags = sorted(list(set([tag for tag in raw_tags.split(',') if tag.isalnum()])))
            self._archive_name_data = ArchiveNameData(source_name, time_stamp, tags)
        return self._archive_name_data

    @property
    def source_name(self) -> Text:
        return self.archive_name_data.source_name

    @property
    def time_stamp(self) -> float:
        if self.archive_name_data.time_stamp is not None:
            return self.archive_name_data.time_stamp
        return self.file_time

    @property
    def tags(self) -> List[Text]:
        return self.archive_name_data.tags

    @classmethod
    def get_method(cls, archive_path: Text, assumed_type: int = None) -> RegisteredMethod:
        for name, method_cls in METHOD_MAP.items():
            base_path = method_cls.check_supported(
                archive_path, assumed_type=assumed_type)
            if base_path:
                return RegisteredMethod(name, method_cls)
        raise ValueError(f'No suitable archive method for "{archive_path}".')

    @classmethod
    def new(cls, path: Text) -> 'DiscoveredArchive':
        """
        Create DiscoveredArchive for physical file or folder.

        :param path: path to archive file or folder
        :return: DiscoveredArchive instance.
        :raise ValueError: when the input is not a valid archive
        """
        registered_method = cls.get_method(path)
        file_stat = os.stat(path)
        return cls(path=path,
                   file_time=file_stat.st_mtime,
                   file_size=file_stat.st_size,
                   method_name=registered_method.name,
                   method_cls=registered_method.method_cls)

    @classmethod
    def new_fake_file(cls,
                      path: Text,
                      file_size: int,
                      file_time: float) -> 'DiscoveredArchive':
        """
        Create DiscoveredArchive for fake file.

        :param path: path to archive file or folder
        :param file_size: size in bytes
        :param file_time: time as float seconds
        :return: DiscoveredArchive instance.
        :raise ValueError: when the input is not a valid archive
        """
        registered_method = cls.get_method(path, assumed_type=1)
        return cls(path=path,
                   file_time=file_time,
                   file_size=file_size,
                   method_name=registered_method.name,
                   method_cls=registered_method.method_cls)

    @classmethod
    def new_fake_folder(cls,
                        path: Text,
                        file_time: float) -> 'DiscoveredArchive':
        """
        Create DiscoveredArchive for fake folder.

        :param path: path to archive file or folder
        :param file_time: time as float seconds
        :return: DiscoveredArchive instance.
        :raise ValueError: when the input is not a valid archive
        """
        registered_method = cls.get_method(path, assumed_type=2)
        return cls(path=path,
                   file_time=file_time,
                   file_size=0,
                   method_name=registered_method.name,
                   method_cls=registered_method.method_cls)
