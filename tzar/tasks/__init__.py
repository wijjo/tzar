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

"""
Tzar root task.
"""

import jiig

from . import catalog, compare, delete, list, prune, save


@jiig.task(tasks=(catalog, compare, delete, list, prune, save))
def root(_runtime: jiig.Runtime):
    """
    Tzar root task.

    [^age_option]: Age strings are one or more summed values separated by '+'.
    A value is a number trailed by a "ymwdHMS" unit letter.

    [^destructive]: Destructive operations require confirmation by default.
    """
    pass
