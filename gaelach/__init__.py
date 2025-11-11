"""
gaelach: a siuba alternative for pandas
"""

# core imports
from gaelach.core.symbolic import _, Symbolic
from gaelach.core import pipe

# acutis imports 
from gaelach import acutis
from gaelach.acutis.affiche import affiche
from gaelach.acutis.count_na import count_na
from gaelach.acutis.count_table import count_table
from gaelach.acutis.pasteurize import pasteurize

# verb imports
from gaelach.verbs.select import select
from gaelach.verbs.mutate import mutate, across
from gaelach.verbs.filter import filter
# from gaelach.verbs.arrange import arrange
# from gaelach.verbs.rename import rename
# from gaelach.verbs.group_by import group_by
# from gaelach.verbs.summarize import summarize
# from gaelach.verbs.round import round
# from gaelach.verbs.head import head
# from gaelach.verbs.tail import tail
# from gaelach.verbs.distinct import distinct 
# from gaelach.verbs.slice import slice
# from gaelach.verbs.relocate import relocate 
# from gaelach.verbs.drop_na import drop_na
# from gaelach.verbs.pull import pull
# from gaelach.verbs.sample import sample
# from gaelach.verbs.join import join
# from gaelach.verbs.pivot import pivot_longer, pivot_wider
# from gaelach.verbs.unite import unite
# from gaelach.verbs.separate import separate
# from gaelach.verbs.bind_cols import bind_cols
# from gaelach.verbs.bind_rows import bind_rows
# from gaelach.verbs.reframe import reframe

# utils + helper imports
from gaelach.utils.helpers import starts_with, ends_with, contains, where, is_boolean, is_cat, \
   is_float, is_integer, is_numeric, is_string, is_temporal, all
# from gaelach.utils.if_else import if_else
# from gaelach.utils.case_when import case_when
# from gaelach.utils.row_contains import row_contains
    
# set version
__version__ = "0.1.0"

# add to primary import 
__all__ = ['_', 'Symbolic', 'select', 'mutate', 'filter', 'across', 'where', 'is_boolean', 
           'is_cat', 'is_float', 'is_integer', 'is_numeric', 'is_string', 'is_temporal', 
           'all', 'starts_with', 'ends_with', 'contains', 'affiche', 'count_na', 'count_table',
           'pasteurize'
           # 'is_null', 'if_else', 'is_null',  
           # 'arrange', 'rename', 'group_by',
           # 'summarize', 'round', 'head', 'tail', 'distinct', 'slice', 'relocate', 'drop_na',
           # 'pull', 'sample', 'pasteurize', 'count_table', 'case_when', 'join', 'pivot_longer', 'pivot_wider', 
           # 'unite', 'separate', 'bind_rows', 'bind_cols', 
           # 'row_contains', 'reframe'
        ]