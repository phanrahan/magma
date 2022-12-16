from dataclasses import dataclass
import uinspect
import collections

from magma.config import config, RuntimeConfig


@dataclass
class _DebugInfo:
    filename: str
    lineno: int
    module: str


debug_info = _DebugInfo


config.register(use_uinspect=RuntimeConfig(True))


def get_debug_info(frames_to_skip):
    if config.use_uinspect:
        filename, lineno = uinspect.get_location(frames_to_skip)
    else:
        filename, lineno = None, None
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
