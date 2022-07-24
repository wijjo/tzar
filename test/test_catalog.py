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

import os
from time import strptime, mktime
import unittest
from typing import List, Text, Optional

from tzar.discovered_archive import DiscoveredArchive
from tzar.runtime import TzarRuntime


class TestCatalog(unittest.TestCase):

    @staticmethod
    def assertList(names: List[Text],
                   expected: List[Text],
                   time_min: Text = None,
                   time_max: Text = None,
                   interval_min: float = None,
                   interval_max: float = None,
                   tags: Optional[Text] = None):
        archives: List[DiscoveredArchive] = []
        for name in names:
            if name.endswith('/'):
                archives.append(DiscoveredArchive.new_fake_folder(
                    f'/my/archives/{name[:-1]}', file_time=0.0))
            else:
                archives.append(DiscoveredArchive.new_fake_file(
                    f'/my/archives/{name}', file_size=0, file_time=0.0))
        filter_tag_set = set(tags.split(',')) if tags else None
        if time_min:
            timestamp_min = mktime(strptime(time_min, '%Y%m%d-%H%M%S'))
        else:
            timestamp_min = None
        if time_max:
            timestamp_max = mktime(strptime(time_max, '%Y%m%d-%H%M%S'))
        else:
            timestamp_max = None
        items = TzarRuntime.build_catalog_list(archives,
                                               'test',
                                               timestamp_min=timestamp_min,
                                               timestamp_max=timestamp_max,
                                               interval_min=interval_min,
                                               interval_max=interval_max,
                                               filter_tag_set=filter_tag_set)
        actual = [os.path.basename(item.path) for item in items]
        if actual != expected:
            raise AssertionError(f'Mismatch: actual={actual} expected={expected}')

    def test_empty(self):
        self.assertList([], [])

    def test_multiple_source_names(self):
        self.assertList(
            [
                'aaa_20191232-000000.tar.xz',
                'test_20191232-000000.tar.xz',
            ],
            [
                'test_20191232-000000.tar.xz',
            ]
        )

    def test_time_stamp_filtering(self):
        self.assertList(
            [
                'test_20200227-000000/',
                'test_20200224-020202/',
                'test_20200311-090909/',
                'test_20200303-123456/',
            ],
            [
                'test_20200303-123456',
                'test_20200227-000000',
            ],
            time_min='20200224-020203',
            time_max='20200303-123456',
        )

    def test_interval_filtering(self):
        self.assertList(
            [
                'test_20200327-000000_zzz.zip',
                'test_20200328-000000.zip',
                'test_20200329-000000.zip',
                'test_20200329-000005.zip',
                'test_20200329-000500.zip',
                'test_20200329-010459.zip',
                'test_20200329-020458.zip',
                'test_20200329-030458.zip',
                'test_20200331-230001.zip',
                'test_20200401-000000.zip',
                'test_20200401-000001.zip',
            ],
            [
                'test_20200401-000001.zip',
                'test_20200329-030458.zip',
                'test_20200329-020458.zip',
                'test_20200328-000000.zip',
                'test_20200327-000000_zzz.zip',
            ],
            interval_min=3600,
        )

    def test_tag_filtering(self):
        test_list = [
            'test_20200327-000000_a,word.zip',
            'test_20200328-000000_the,a.zip',
            'test_20200329-000000.zip',
            'test_20200329-000005_words,blah.zip',
            'test_20200329-000500_abc.zip',
            'test_20200329-010459_sword.zip',
            'test_20200329-020458.fluff,muggle,fluffy.zip',
            'test_20200329-030458_abc,def,ghi.zip',
            'test_20200331-230001_.zip',
            'test_20200401-000000_a,abc.zip',
        ]

        self.assertList(
            test_list,
            [
            ],
            tags='m'
        )

        self.assertList(
            test_list,
            [
                'test_20200401-000000_a,abc.zip',
                'test_20200328-000000_the,a.zip',
                'test_20200327-000000_a,word.zip',
            ],
            tags='a'

        )

        self.assertList(
            test_list,
            [
                'test_20200327-000000_a,word.zip',
            ],
            tags='a,word'

        )
