import inspect
import sys


def debug_wire(fn):
    """
    Automatically populates the `debug_info` argument for a wire call if it's
    not already passed as an argument
    """
    # TODO: We could check that fn has the correct interface 
    #       wire(i, o, debug_info)
    def wire(i, o, debug_info=None):
        if debug_info is None:
            callee_frame = inspect.stack()[1]
            if sys.version_info < (3, 5):
                callee_frame = inspect.getframeinfo(frame)
            debug_info = callee_frame.filename, callee_frame.lineno
        return fn(i, o, debug_info)
    return wire

