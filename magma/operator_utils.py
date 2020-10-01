import functools


def output_only(err_msg):
    def wrapper(fn):
        @functools.wraps(fn)
        def wrapped(self, *args, **kwargs):
            if self.is_input():
                raise TypeError(err_msg)
            return fn(self, *args, **kwargs)
        return wrapped
    return wrapper
