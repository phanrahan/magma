import collections
import dataclasses
import functools
from typing import Any, Callable, Dict, Iterable, Optional, Tuple


def wrap_with_not_implemented_error(fn):

    @functools.wraps(fn)
    def wrapped(*args, **kwargs):
        ret = fn(*args, **kwargs)
        if ret is None:
            raise NotImplementedError(args, kwargs)
        return ret

    return wrapped


_unique_name_index = 0


def make_unique_name() -> str:
    global _unique_name_index
    name = "%032d" % _unique_name_index
    _unique_name_index += 1
    return name


def default_field(cons, **kwargs):
    return dataclasses.field(default_factory=cons, **kwargs)


@dataclasses.dataclass
class WithId:
    id: str = dataclasses.field(default_factory=make_unique_name, init=False)


def constant(value: Any):
    return lambda: value


def try_call(fn: Callable[[], Any], ExceptionType: Optional[Any]):
    if ExceptionType is None:
        ExceptionType = BaseException
    try:
        ret = fn()
    except ExceptionType:
        pass
    else:
        return ret
