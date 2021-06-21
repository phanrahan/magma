import functools


def output_only(msg):

    def _wrapper(fn):

        @functools.wraps(fn)
        def _wrapped(self, *args, **kwargs):
            if self.is_input():
                raise TypeError(msg)
            return fn(self, *args, **kwargs)

        return _wrapped

    return _wrapper
