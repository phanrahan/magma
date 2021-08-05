from magma.array import Array
from magma.tuple import Tuple


def _make_unconnected_error_str(port):
    error_str = port.debug_name
    if port.trace() is not None:
        error_str += ": Connected"
    elif isinstance(port, (Tuple, Array)):
        child_str = ""
        for child in port:
            child = _make_unconnected_error_str(child)
            child = "\n    ".join(child.splitlines())
            child_str += f"\n    {child}"
        if "Connected" not in child_str:
            # Handle case when no children are connected (simplify)
            error_str += ": Unconnected"
        else:
            error_str += child_str
    elif port.trace() is None:
        error_str += ": Unconnected"
    return error_str


class MagmaCompileException(Exception):
    pass


class UnconnectedPortException(MagmaCompileException):
    def __init__(self, port):
        msg = f"Found unconnected port: {port.debug_name}\n"
        msg += _make_unconnected_error_str(port)
        super().__init__(msg)
