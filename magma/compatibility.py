import sys

__all__ = ['IntegerTypes', 'StringTypes']

if sys.version_info < (3,):
    IntegerTypes = (int, long)
    StringTypes = (str, unicode)
    long = long
    import __builtin__ as builtins
else:
    IntegerTypes = (int,)
    StringTypes = (str,)
    long = int
    import builtins
