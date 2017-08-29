from __future__ import print_function
import traceback
import inspect
import sys

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

def warn(*args):
    print(*args)
    traceback.print_stack()

def error(message):
    stack_frame = get_original_wire_call_stack_frame()
    sys.stderr.write("="*80 + "\n")
    traceback.print_stack(f=stack_frame, limit=10)
    sys.stderr.write(message + "\n")
    sys.stderr.write("="*80 + "\n")
