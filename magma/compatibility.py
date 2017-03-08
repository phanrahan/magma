import sys

__all__ = ['IntegerTypes', 'StringTypes']

if sys.version_info < (3,):
    IntegerTypes = (int, long)
    StringTypes = (str, unicode)
else:
    IntegerTypes = (int,)
    StringTypes = (str,)

