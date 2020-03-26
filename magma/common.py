import collections
from functools import wraps, partial
import warnings


class Stack:
    """Lightweight wrapper over builtin lists to provide a stack interface"""
    def __init__(self):
        self._stack = []

    def push(self, value):
        self._stack.append(value)

    def pop(self):
        return self._stack.pop()

    def peek(self):
        return self._stack[-1]


class _Ref(object):
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value is other.value

    def __hash__(self):
        return id(self.value)


class IdentitySet(collections.MutableSet):
    def __init__(self, items=[]):
        self.refs = set(map(_Ref, items))

    def __contains__(self, elem):
        return _Ref(elem) in self.refs

    def __iter__(self):
        return (ref.value for ref in self.refs)

    def __len__(self):
        return len(self.refs)

    def add(self, elem):
        self.refs.add(_Ref(elem))

    def discard(self, elem):
        self.refs.discard(_Ref(elem))

    def __repr__(self):
        return "%s(%s)" % (type(self).__name__, list(self))


def deprecated(func=None, *, msg=None):
    """
    Inspired by https://pybit.es/decorator-optional-argument.html.

    Marks a function as deprecated. @msg is an optional parameter to override
    the default warning.

    Examples:

        @deprecated
        def foo(...): ...

        @deprecated('Don't use bar!')
        def bar(...): ...
    """
    if func is None:
        return partial(deprecated, msg=msg)
    if msg is None:
        msg = f"{func.__name__} is deprecated"

    @wraps(func)
    def _wrapper(*args, **kwargs):
        warnings.warn(msg, category=DeprecationWarning, stacklevel=2)
        return func(*args, **kwargs)

    return _wrapper


def setattrs(obj, dct, pred=None):
    for k, v in dct.items():
        if pred is None or pred(k, v):
            setattr(obj, k, v)
