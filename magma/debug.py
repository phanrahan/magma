<<<<<<< Updated upstream
import uinspect
=======
import dataclasses
import inspect
>>>>>>> Stashed changes
import collections


<<<<<<< Updated upstream
debug_info = collections.namedtuple("debug_info",
                                    ["filename", "lineno", "module"])
=======
@dataclasess
class _DebugInfo:
    filename: str
    lineno: int
    module: str


debug_info = _DebugInfo
>>>>>>> Stashed changes


def get_debug_info(frames_to_skip):
    filename, lineno = uinspect.get_location(frames_to_skip)
    return debug_info(filename, lineno, None)


def debug_wire(fn):
    """
    Automatically populates the `debug_info` argument for a wire call if it's
    not already passed as an argument
    """
    def wire(i, o=None, debug_info=None):
        if debug_info is None:
            debug_info = get_debug_info(3)
        return fn(i, o, debug_info)
    return wire


def debug_unwire(fn):
    def unwire(i, o=None, debug_info=None, keep_wired_when_contexts=False):
        if debug_info is None:
            debug_info = get_debug_info(3)
        return fn(i, o, debug_info, keep_wired_when_contexts)
    return unwire
