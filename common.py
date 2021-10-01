import functools
from typing import Any, Dict, Iterable, Tuple


_MISSING = object()


def wrap_with_not_implemented_error(fn):

    @functools.wraps(fn)
    def wrapped(*args, **kwargs):
        ret = fn(*args, **kwargs)
        if ret is None:
            raise NotImplementedError(args, kwargs)
        return ret

    return wrapped


def missing() -> object:
    global _MISSING
    return _MISSING


_unique_name_index = 0


def make_unique_name() -> str:
    global _unique_name_index
    name = "%032d" % _unique_name_index
    _unique_name_index += 1
    return name
