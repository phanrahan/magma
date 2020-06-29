from typing import Optional

from ast_tools.stack import SymbolTable
from ast_tools.passes import apply_ast_passes, ssa, if_to_phi, bool_to_bit

from ..circuit import Circuit, IO
from ..clock_io import ClockIO
from ..t import Type, Direction
from ..protocol_type import MagmaProtocol, MagmaProtocolMeta
from ..primitives.register import Register

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


class _SequentialRegisterWrapperMeta(MagmaProtocolMeta):
    def _to_magma_(cls):
        return cls.T

    def _qualify_magma_(cls, direction: Direction):
        return cls[cls.T.qualify(direction)]

    def _flip_magma_(cls):
        return cls[cls.T.flip()]

    def _from_magma_value_(cls, val: Type):
        return cls(val)

    def __getitem__(cls, T):
        return type(cls)(f"_SequentialRegisterWrapper{T}", (cls, ), {"T": T})


class _SequentialRegisterWrapper(MagmaProtocol,
                                 metaclass=_SequentialRegisterWrapperMeta):
    """
    Wraps sequential attributes to implement register getattr syntax and
    general circuit call syntax, e.g.

        def __init__(self):
            self.x = Register(4)

        def __call__(self, ...) -> ...:
            if S:
                return self.x(I)  # call syntax
            return self.x + 1     # attribute syntax
    """

    def __init__(self, circuit: Circuit):
        self.circuit = circuit

    def _get_magma_value_(self):
        # Return output
        return self.circuit()

    # TODO: Clever way to pass through operators to the underlying value?
    def __add__(self, other):
        return self._get_magma_value_() + other

    def __sub__(self, other):
        return self._get_magma_value_() - other

    def __mul__(self, other):
        return self._get_magma_value_() * other

    def __truediv__(self, other):
        return self._get_magma_value_() / other

    def __floordiv__(self, other):
        return self._get_magma_value_() // other

    def __mod__(self, other):
        return self._get_magma_value_() % other

    def __or__(self, other):
        return self._get_magma_value_() | other

    def __xor__(self, other):
        return self._get_magma_value_() ^ other

    def __and__(self, other):
        return self._get_magma_value_() & other

    def __eq__(self, other):
        return self._get_magma_value_() == other

    def __ne__(self, other):
        return self._get_magma_value_() != other

    def __ge__(self, other):
        return self._get_magma_value_() >= other

    def __gt__(self, other):
        return self._get_magma_value_() > other

    def __le__(self, other):
        return self._get_magma_value_() <= other

    def __lt__(self, other):
        return self._get_magma_value_() < other

    def __lshift__(self, other):
        return self._get_magma_value_() << other

    def __rshift__(self, other):
        return self._get_magma_value_() >> other

    def __neg__(self, other):
        return -self._get_magma_value_()

    def __invert__(self, other):
        return ~self._get_magma_value_()

    def ite(self, s, t, f):
        return self._get_magma_value_().ite(s, t, f)

    def __call__(self, *args, **kwargs):
        return self.circuit(*args, **kwargs)

    def __getitem__(self, i):
        key = i._get_magma_value_() if isinstance(i, MagmaProtocol) else i
        return self._get_magma_value_()[key]


def sequential_getattribute(self, key):
    """
    Wrap lists so we can use the setattr interface with lists of registers
    """
    result = object.__getattribute__(self, key)
    if isinstance(result, list):
        return _SequentialListWrapper(result)
    if isinstance(type(result), Register):
        return _SequentialRegisterWrapper[type(result())](result)
    return result


def sequential_setattr(self, key, value):
    # TODO: for now we assume this is a register, ideally we'd type check this,
    # but we need to have a notion of a register primitive (e.g. right now the
    # mantle reg wraps the coreir reg primitive, so technically the register is
    # an arbitrary user-defined circuit)

    target = object.__getattribute__(self, key)
    # We can at least match the value is a circuit with outputs that match the
    # input of the attribute circuit
    if not isinstance(target, Circuit):
        raise TypeError("Excepted setattr key to be a Circuit")

    if isinstance(value, MagmaProtocol):
        value = value._get_magma_value_()
    if not isinstance(value, (Circuit, int, Type)):
        raise TypeError("Excepted setattr value to be a Circuit, Type, or int",
                        f"not {type(value)}")

    # Simply use function call syntax for now (should automatically retrieve
    # the output of value)
    target(value)


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
    if isinstance(t, tuple):
        assert isinstance(f, tuple)
        return tuple(_seq_phi(s, _t, _f) for _t, _f in zip(t, f))
    # Unpack registers/circuits used in getattr syntax
    t, f = map(_process_phi_arg, (t, f))
    return s.ite(t, f)


def sequential2(pre_passes=[], post_passes=[],
                debug: bool = False,
                env: Optional[SymbolTable] = None,
                path: Optional[str] = None,
                file_name: Optional[str] = None,
                annotations: Optional[dict] = None,
                **clock_io_kwargs):
    """ clock_io_kwargs used for ClockIO params, e.g. async_reset """
    passes = (pre_passes +
              [ssa(strict=False), bool_to_bit(), if_to_phi(_seq_phi)] +
              post_passes)

    def seq_inner(cls):
        cls.__call__ = apply_ast_passes(passes, debug=debug, env=env,
                                        path=path,
                                        file_name=file_name)(cls.__call__)
        if annotations is None:
            _annotations = cls.__call__.__annotations__
        else:
            _annotations = annotations

        if "self" in _annotations:
            raise Exception("Assumed self did not have annotation")

        io_args = build_io_args(_annotations)

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

            call_args += build_call_args(io, _annotations)

            call_result = cls.__call__(*call_args)
            wire_call_result(io, call_result, cls.__call__.__annotations__)
        return SequentialCircuit
    return seq_inner
