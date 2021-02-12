"""
Tzar root task.
"""

import jiig

from . import catalog, compare, delete, list, prune, save

TASK = jiig.Task(
    description='Tzar root task.',

    tasks={
        'catalog': catalog,
        'compare': compare,
        'delete': delete,
        'list': list,
        'prune': prune,
        'save': save,
        'alias[s]': jiig.task.alias,
        'help[s]': jiig.task.help,
        'unittest[h]': jiig.task.unittest,
        'venv[h]': jiig.task.venv,
    },

    footnotes={
        'age_option': '''
Age strings are one or more summed values separated by '+'. A value is a number
trailed by a "ymwdHMS" unit letter.
''',
        'destructive': 'Destructive operations require confirmation by default.',
    }
)
