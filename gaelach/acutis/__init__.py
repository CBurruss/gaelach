"""
Acutis module: Extended methods for Pandas objects.

Importing this module adds additional methods to Pandas Series and DataFrame objects.
"""

from gaelach.acutis.affiche import affiche             # Imports both the function and the method 
from gaelach.acutis.count_na import count_na
from gaelach.acutis.count_table import count_table
from gaelach.acutis.pasteurize import pasteurize

__all__ = ['affiche', 'count_na', 'count_table', 'pasteurize']