import functools


def wrap_with_not_implemented_error(fn):

    @functools.wraps(fn)
    def wrapped(*args, **kwargs):
        ret = fn(*args, **kwargs)
        if ret is None:
            raise NotImplementedError(args, kwargs)
        return ret

    return wrapped
