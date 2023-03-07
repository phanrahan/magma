from typing import Sequence, Union

import hwtypes as ht
from hwtypes import BitVector, UIntVector, SIntVector

from magma.array import Array
from magma.bit import Bit
from magma.bits import Bits, UInt, SInt
from magma.bitutils import clog2, seq2int
from magma.circuit import coreir_port_mapping
from magma.common import is_int
from magma.debug import magma_helper_function
from magma.generator import Generator2
from magma.interface import IO
from magma.protocol_type import MagmaProtocol, magma_type
from magma.t import Type, In, Out, Direction
from magma.tuple import Product, Tuple
from magma.type_utils import type_to_sanitized_string
from magma.conversions import tuple_, as_bits, from_bits


class CoreIRCommonLibMuxN(Generator2):
    def __init__(self, N: int, width: int):
        self.name = f"coreir_commonlib_mux{N}x{width}"
        FlatT = Array[width, Bit]
        MuxInT = Product.from_fields("anon", dict(data=Array[N, FlatT],
                                                  sel=Bits[clog2(N)]))
        self.io = IO(I=In(MuxInT), O=Out(Bits[width]))
        self.renamed_ports = coreir_port_mapping
        self.coreir_name = "muxn"
        self.coreir_lib = "commonlib"
        self.coreir_genargs = {"width": width, "N": N}
        self.primitive = True
        self.stateful = False

        def simulate(self, value_store, state_store):
            sel = BitVector[clog2(N)](value_store.get_value(self.I.sel))
            out = BitVector[width](value_store.get_value(self.I.data[int(sel)]))
            value_store.set_value(self.O, out)

        self.simulate = simulate


class Mux(Generator2):
    def __init__(self, height: int, T: Type):
        if issubclass(T, BitVector):
            T = Bits[len(T)]
        if issubclass(T, (bool, ht.Bit)):
            T = Bit

        # TODO(rsetaluri): Type should be hashable so the generator instance can
        # be cached.
        T_str = type_to_sanitized_string(T)
        self.name = f"Mux{height}x{T_str}"

        ports = {f"I{i}": In(T) for i in range(height)}
        T_S = Bit if height == 2 else Bits[clog2(height)]
        ports["S"] = In(T_S)
        ports["O"] = Out(T)

        self.io = IO(**ports)

        self.height = height
        self.T = T

        self.primitive = True
        self.stateful = False

        def _simulate(_, __, ___):
            raise NotImplementedError()

        self.simulate = _simulate

    def elaborate(self):
        N = magma_type(self.T).flat_length()
        mux = CoreIRCommonLibMuxN(self.height, N)()
        data = [as_bits(self.io[f"I{i}"]) for i in range(self.height)]
        mux.I.data @= Array[self.height, Bits[N]](data)
        sel = mux.I.sel
        if self.height == 2:
            sel = sel[0]
        sel @= self.io.S
        if issubclass(self.T, MagmaProtocol):
            out = Out(self.T)._from_magma_value_(
                from_bits(self.T._to_magma_(), mux.O)
            )
        else:
            out = from_bits(self.T, mux.O)
        self.io.O @= out


def _infer_mux_type(args):
    """
    Try to infer type by traversing arguments in order:
    * If we encounter a magma Type/Protocol, use that
    * BitVector/Bit/bool are converted to their magma equivalent Bits/Bit
    * Python tuple is converted to m.Tuple (note this will invoke m.tuple_ on
      all the arguments, which may raise an error if the tuple arguments are
      not well formed)

    Note that we do not infer from standard python int arguments because we
    cannot, in general, determine the correct bit width (use BitVector instead)
    """
    T = None
    for arg in args:
        if isinstance(arg, (Type, MagmaProtocol)):
            next_T = type(arg).qualify(Direction.Undirected)
        elif isinstance(arg, UIntVector):
            next_T = UInt[len(arg)]
        elif isinstance(arg, SIntVector):
            next_T = SInt[len(arg)]
        elif isinstance(arg, BitVector):
            next_T = Bits[len(arg)]
        elif isinstance(arg, (ht.Bit, bool)):
            next_T = Bit
        elif isinstance(arg, tuple):
            next_T = type(tuple_(arg))
        elif isinstance(arg, int):
            # Cannot infer type without width, use wiring implicit coercion to
            # handle (or raise type error there)
            continue

        if T is not None:
            if issubclass(T, next_T):
                # upcast
                T = next_T
            elif not next_T.is_wireable(T) and not T.is_wireable(next_T):
                raise TypeError(
                    f"Found incompatible types {next_T} and {T} in mux"
                    " inference"
                )
        else:
            T = next_T
    if T is None:
        raise TypeError(
            f"Could not infer mux type from {args}\n"
            "Need at least one magma value, BitVector, bool or tuple")
    if issubclass(T, Tuple):
        args = [tuple_(a) for a in args]
    return T, args


infer_mux_type = _infer_mux_type


@magma_helper_function
def mux(I: Union[Sequence, Array], S, **kwargs):
    """
    How type inference works on I:
        This operator will traverse the list of inputs I and use the first
        magma value to determine the type.  This allows I to contain coerceable
        objects like ints (e.g. `mux([1, x], s)` where `x: UInt[2]`).  Coercion
        is peformed when wiring the arguments to the input of an instance of
        Mux(T) (where T is the type of the first magma value) and will raise an
        error there if one of the values cannot be coerced to T.
        **NOTE** This will fail if the type of the first magma value cannot
        coerce subsequent arguments (even though the type of a later argument
        might be able to coerce the type of the earliest argument).  We plan to
        improve the algorithm to support the more general cases, but until
        then, if you run into this problem, use `Mux(T)` where `T` can coerce
        all arguments.
    """
    if is_int(S):
        return I[int(S)]
    T, I = _infer_mux_type(I)
    inst = Mux(len(I), T)(**kwargs)
    if len(I) == 2 and isinstance(S, Bits[1]):
        S = S[0]
    result = inst(*I, S)
    for i in range(len(I)):
        if getattr(inst, f"I{i}").value() is None:
            arg = I[i]
            raise TypeError(f"mux arg I[{i}] ({arg}: {type(arg)}) does not "
                            f"match inferred input port type {T}")
    return result


# Monkey patch for ite impl without circular dependency
Bit._mux = staticmethod(mux)


# NOTE(rsetaluri): We monkeypatch this function on to Array due to the circular
# dependency between Mux and Array. See the discussion on
# https://github.com/phanrahan/magma/pull/658.
@magma_helper_function
def _dynamic_mux_select(this, key):
    return mux(this.ts, key)


Array.dynamic_mux_select = _dynamic_mux_select


@magma_helper_function
def dict_lookup(dict_, select, default=0):
    """
    Use `select` as an index into `dict` (similar to a case statement)

    `default` is used when `select` does not match any of the keys and has a
    default value of 0
    """
    output = default
    for key, value in dict_.items():
        output = mux([output, value], key == select)
    return output


@magma_helper_function
def list_lookup(list_, select, default=0):
    """
    Use `select` as an index into `list` (similar to a case statement)

    `default` is used when `select` does not match any of the indices (e.g.
    when the select width is longer than the list) and has a default value of
    0.
    """
    output = default
    for i, elem in enumerate(list_):
        output = mux([output, elem], i == select)
    return output
