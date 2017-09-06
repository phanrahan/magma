from __future__ import absolute_import

import logging
import traceback
import inspect
import sys

log = logging.getLogger("magma")
def get_original_wire_call_stack_frame():
    for frame in inspect.stack():
        if sys.version_info < (3, 5):
            function = inspect.getframeinfo(frame[0]).function
        else:
            function = frame.function
        if function not in ["wire", "connect",
                            "get_original_wire_call_stack_frame",
                            "error", "warn"]:
            break
    if sys.version_info < (3, 5):
        return frame[0]
    else:
        return frame.frame

def info(message, *args, **kwargs):
    log.info(message, *args, **kwargs)

def warning(message, *args, **kwargs):
    log.warning(message, *args, **kwargs)

def error(message, include_wire_traceback=False, *args, **kwargs):
    if include_wire_traceback:
        sys.stderr.write("="*80 + "\n")
        stack_frame = get_original_wire_call_stack_frame()
        traceback.print_stack(f=stack_frame, limit=10, file=sys.stderr)
    log.error(message, *args, **kwargs)
    if include_wire_traceback:
        sys.stderr.write("="*80 + "\n")
