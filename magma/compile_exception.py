from magma.array import Array
from magma.tuple import Tuple


def make_unconnected_error_str(port):
    format_args = [port]
    error_str = "{}"
    if port.trace() is not None:
        error_str += ": Connected"
    elif isinstance(port, (Tuple, Array)):
        child_str = ""
        for child in port:
            child, child_args = make_unconnected_error_str(child)
            format_args.extend(child_args)
            child = "\n    ".join(child.splitlines())
            child_str += f"\n    {child}"
        if "Connected" not in child_str:
            # Handle case when no children are connected (simplify)
            error_str += ": Unconnected"
        else:
            error_str += child_str
    elif port.trace() is None:
        error_str += ": Unconnected"
    return error_str, format_args


class MagmaCompileException(Exception):
    pass


class UnconnectedPortException(MagmaCompileException):
    def __init__(self, port):
        msg = f"Found unconnected port: {port.debug_name}\n"
        error_str, format_args = make_unconnected_error_str(port)
        msg += error_str.format(*(arg.debug_name for arg in format_args))
        super().__init__(msg)
