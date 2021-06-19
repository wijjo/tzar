"""
Tzar root task.
"""

import jiig

from . import catalog, compare, delete, list, prune, save


class Task(
    jiig.Task,
    tasks={
        'catalog': catalog,
        'compare': compare,
        'delete': delete,
        'list': list,
        'prune': prune,
        'save': save,
        'unittest[h]': jiig.tasks.unittest,
    },
    footnotes={
        'age_option': '''
Age strings are one or more summed values separated by '+'. A value is a number
trailed by a "ymwdHMS" unit letter.
''',
        'destructive': 'Destructive operations require confirmation by default.',
    }
):
    """Tzar root task."""
    pass
