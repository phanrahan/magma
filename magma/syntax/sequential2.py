from typing import Optional

from ast_tools.stack import SymbolTable
from ast_tools.passes import apply_ast_passes, ssa, if_to_phi, bool_to_bit

from ..circuit import Circuit, IO
from ..clock_io import ClockIO
from ..t import Type

from .util import build_io_args, build_call_args, wire_call_result


class _SequentialListWrapper(list):
    def __getitem__(self, i):
        result = super().__getitem__(i)
        if isinstance(result, list):
            return _SequentialListWrapper(result)
        return result

    def __setitem__(self, i, value):
        item = self[i]
        if not isinstance(item, Circuit):
            raise TypeError("Excepted setitem target to be a Circuit")

        if not isinstance(value, (Circuit, int, Type)):
            raise TypeError("Excepted setitem value to be a Circuit, Type, or "
                            f"int, not {type(value)}")

        item(value)


def sequential_getattribute(self, key):
    """
    Wrap lists so we can use the setattr interface with lists of registers
    """
    result = object.__getattribute__(self, key)
    if isinstance(result, list):
        return _SequentialListWrapper(result)
    return result


def sequential_setattr(self, key, value):
    # TODO: for now we assume this is a register, ideally we'd type check this,
    # but we need to have a notion of a register primitive (e.g. right now the
    # mantle reg wraps the coreir reg primitive, so technically the register is
    # an arbitrary user-defined circuit)

    # We can at least match the value is a circuit with outputs that match the
    # input of the attribute circuit
    if not isinstance(getattr(self, key), Circuit):
        raise TypeError("Excepted setattr key to be a Circuit")

    if not isinstance(value, (Circuit, int, Type)):
        raise TypeError("Excepted setattr value to be a Circuit, Type, or int",
                        f"not {type(value)}")

    # Simply use function call syntax for now (should automatically retrieve
    # the output of value)
    getattr(self, key)(value)


def _process_phi_arg(arg):
    if isinstance(arg, Circuit):
        # Call with no args to retrieve output(s)
        arg = arg()
        if isinstance(arg, list):
            # TODO: We could support tuples/products
            raise TypeError("Cannot use circuit with multiple outputs as "
                            "argument to phi")
    return arg


def _seq_phi(s, t, f):
    # Unpack registers/circuits used in getattr syntax
    t, f = map(_process_phi_arg, (t, f))
    return s.ite(t, f)


def sequential2(pre_passes=[], post_passes=[],
                debug: bool = False,
                env: Optional[SymbolTable] = None,
                path: Optional[str] = None,
                file_name: Optional[str] = None,
                **clock_io_kwargs):
    """ clock_io_kwargs used for ClockIO params, e.g. async_reset """
    passes = (pre_passes +
              [ssa(strict=False), bool_to_bit(), if_to_phi(_seq_phi)] +
              post_passes)

    def seq_inner(cls):
        cls.__call__ = apply_ast_passes(passes, debug=debug, env=env,
                                        path=path,
                                        file_name=file_name)(cls.__call__)

        if "self" in cls.__call__.__annotations__:
            raise Exception("Assumed self did not have annotation")

        io_args = build_io_args(cls.__call__.__annotations__)

        class SequentialCircuit(Circuit):
            name = cls.__name__
            io = IO(**io_args) + ClockIO(**clock_io_kwargs)
            call_args = [cls()]

            # Monkey patch setattribute for register assign syntax, we could
            # also add this in a Sequential base class, but if we do that we
            # might as well use a metaclass rather than a decorator, but to
            # preserve the old interface we do this for now
            cls.__setattr__ = sequential_setattr

            # also need to patch getattr to support list attributes (see
            # test_sequential2:test_sequential2_pre_unroll)
            cls.__getattribute__ = sequential_getattribute

            call_args += build_call_args(io, cls.__call__.__annotations__)

            call_result = cls.__call__(*call_args)
            wire_call_result(io, call_result, cls.__call__.__annotations__)
        return SequentialCircuit
    return seq_inner
