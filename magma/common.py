from functools import wraps, partial
import warnings


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
