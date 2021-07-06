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
