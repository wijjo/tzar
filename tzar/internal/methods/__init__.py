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

"""Archive support package."""

from .base import (
    ArchiveMethodBase,
    MethodListItem,
    MethodSaveData,
    MethodSaveResult,
)
from .files import ArchiveMethodSync
from .gz import ArchiveMethodGZ
from .xz import ArchiveMethodXZ
from .zip import ArchiveMethodZip
