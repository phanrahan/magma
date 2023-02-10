import collections
import dataclasses
import functools
from typing import Optional
import uinspect

from magma.common import Stack
from magma.config import config, RuntimeConfig


@dataclasses.dataclass
class _DebugInfo:
    filename: str
    lineno: int
    module: str


debug_info = _DebugInfo


config.register(use_uinspect=RuntimeConfig(True))


_extra_frames_to_skip_stack = Stack()


def _get_extra_frames_to_skip_stack():
    global _extra_frames_to_skip_stack
    return _extra_frames_to_skip_stack


def get_debug_info(frames_to_skip):
    extra_frames_to_skip = _get_extra_frames_to_skip_stack().peek_default(0)
    frames_to_skip += extra_frames_to_skip
    if config.use_uinspect:
        filename, lineno = uinspect.get_location(frames_to_skip)
    else:
        filename, lineno = None, None
    return debug_info(filename, lineno, None)


def maybe_get_debug_info(obj) -> Optional[_DebugInfo]:
    """Get the debug_info attribute of @obj if it exists, otherwise None.
    """
    return getattr(obj, "debug_info", None)


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


def _helper_function(fn):

    @functools.wraps(fn)
    def _wrapper(*args, **kwargs):
        extra_frames_to_skip_stack = _get_extra_frames_to_skip_stack()
        # We keep track of the previous frames_to_skip value since the stack is
        # additive.
        try:
            offset = extra_frames_to_skip_stack.peek()
        except IndexError:
            offset = 0
        # NOTE(rsetaluri): We need to skip an extra frame (1 + 1 = 2) since we
        # are returning a wrapped function (decorated).
        extra_frames_to_skip_stack.push(2 + offset)
        try:
            return fn(*args, **kwargs)
        except:
            raise
        finally:
            extra_frames_to_skip_stack.pop()

    return _wrapper


magma_helper_function = _helper_function
