import inspect
import collections
import magma
from magma.config import get_debug_mode


debug_info = collections.namedtuple("debug_info", ["filename", "lineno", "module"])


def get_callee_frame_info():
    stack = inspect.stack()
    # FIXME: Right now we assume a max 10 frames deep
    for i in range(0, 10):
        callee_frame = stack[i][0]
        module = inspect.getmodule(callee_frame)
        # Go up until we're out of the magma module (assuming this is the user
        # code)
        if not module or module.__name__.split(".")[0] != "magma":
            break
    callee_frame = inspect.getframeinfo(callee_frame)
    return debug_info(callee_frame.filename, callee_frame.lineno, module)


def debug_wire(fn):
    """
    Automatically populates the `debug_info` argument for a wire call if it's
    not already passed as an argument
    """
    # TODO: We could check that fn has the correct interface
    #       wire(i, o, debug_info)
    def wire(i, o, debug_info=None):
        if get_debug_mode() and debug_info is None:
            debug_info = get_callee_frame_info()
        return fn(i, o, debug_info)
    return wire

