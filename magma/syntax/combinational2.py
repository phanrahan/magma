import functools

from ast_tools.passes import apply_ast_passes, ssa, if_to_phi, debug

from ..circuit import Circuit, IO
from ..protocol_type import MagmaProtocol
from ..t import Type

from .util import build_io_args, build_call_args, wire_call_result


class combinational2(apply_ast_passes):
    def __init__(self, pre_passes=[], post_passes=[]):
        passes = (pre_passes +
                  [ssa(strict=False), if_to_phi(lambda s, t, f: s.ite(t, f))] +
                  post_passes)
        enable_debug = any(isinstance(x, debug) for x in passes)
        super().__init__(passes=passes, debug=enable_debug)

    def exec(self, *args, **kwargs):
        fn = super().exec(*args, **kwargs)

        io_args = build_io_args(fn.__annotations__)

        class CombinationalCircuit(Circuit):
            name = fn.__name__
            io = IO(**io_args)

            call_args = build_call_args(io, fn.__annotations__)

            call_result = fn(*call_args)

            wire_call_result(io, call_result, fn.__annotations__)

        @functools.wraps(fn)
        def func(*args, **kwargs):
            if (len(args) + len(kwargs) and
                not any(isinstance(x, (Type, MagmaProtocol)) for x in args +
                        tuple(kwargs.values()))):
                # If not called with at least one magma value, use the Python
                # implementation
                return fn(*args, **kwargs)
            return CombinationalCircuit()(*args, **kwargs)
        func.__name__ = fn.__name__
        func.__qualname__ = fn.__name__
        # Provide a mechanism for accessing the underlying circuit definition
        setattr(func, "circuit_definition", CombinationalCircuit)
        return func
