import functools
from typing import Optional

from ast_tools.passes import apply_ast_passes, ssa, if_to_phi, bool_to_bit
from ast_tools.stack import SymbolTable

from ..circuit import Circuit, IO
from ..protocol_type import MagmaProtocol
from ..t import Type

from .util import build_io_args, build_call_args, wire_call_result


class combinational2(apply_ast_passes):
    def __init__(self, pre_passes=[], post_passes=[],
                 debug: bool = False,
                 env: Optional[SymbolTable] = None,
                 path: Optional[str] = None,
                 file_name: Optional[str] = None
                 ):
        passes = (pre_passes +
                  [ssa(strict=False), bool_to_bit(),
                   if_to_phi(lambda s, t, f: s.ite(t, f))] +
                  post_passes)
        super().__init__(passes=passes, env=env, debug=debug, path=path,
                         file_name=file_name)

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
