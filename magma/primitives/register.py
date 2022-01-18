from typing import Union

import coreir
import hwtypes as ht

from magma.array import Array
from magma.bit import Bit
from magma.clock import Enable
from magma.common import ParamDict
from magma.bits import Bits, UInt, SInt
from magma.circuit import coreir_port_mapping
from magma.conversions import as_bits, from_bits, bit
from magma.interface import IO
from magma.generator import Generator2
from magma.t import Type, Kind, In, Out, Direction
from magma.tuple import Tuple
from magma.clock import (AbstractReset,
                         AsyncReset, AsyncResetN, Clock, get_reset_args)
from magma.clock_io import ClockIO
from magma.primitives.mux import Mux
from magma.wire import wire


class _CoreIRRegister(Generator2):
    """
    Internally used generator for CoreIR register primitive
    """
    def __init__(self, width, init=0, has_async_reset=False,
                 has_async_resetn=False):
        self.name = "reg_P"
        self.coreir_configargs = {"init": coreir.type.BitVector[width](init)}
        T = Bits[width]
        self.io = IO(I=In(T), CLK=In(Clock), O=Out(T))

        if has_async_resetn and has_async_reset:
            raise ValueError("Cannot have posedge and negedge asynchronous "
                             "reset")

        if has_async_reset:
            self.io += IO(arst=In(AsyncReset))
            self.name += "R"
            self.coreir_configargs["arst_posedge"] = True

        if has_async_resetn:
            self.io += IO(arst=In(AsyncResetN))
            self.name += "Rn"
            self.coreir_configargs["arst_posedge"] = False

        self.name += f"{width}"

        self.stateful = True
        self.primitive = True
        self.default_kwargs = {"init": coreir.type.BitVector[width](init)}
        self.coreir_genargs = {"width": width}
        self.renamed_ports = coreir_port_mapping

        self.coreir_name = "reg"
        if (has_async_reset or has_async_resetn):
            self.coreir_name += "_arst"

        self.verilog_name = "coreir_" + self.coreir_name
        self.coreir_lib = "coreir"

        def _simulate(self, value_store, state_store):
            cur_clock = value_store.get_value(self.CLK)

            if not state_store:
                state_store['prev_clock'] = cur_clock
                state_store['cur_val'] = ht.BitVector[width](init)

            if has_async_reset or has_async_resetn:
                cur_reset = value_store.get_value(self.arst)

            prev_clock = state_store['prev_clock']
            clock_edge = cur_clock and not prev_clock

            new_val = state_store['cur_val'].as_bool_list()

            if clock_edge:
                new_val = value_store.get_value(self.I)

            if has_async_reset and cur_reset or \
                    has_async_resetn and not cur_reset:
                new_val = ht.BitVector[width](init)

            state_store['prev_clock'] = cur_clock
            state_store['cur_val'] = ht.BitVector[width](new_val)
            value_store.set_value(self.O, new_val)
        self.simulate = _simulate


def _zero_init(T, init):
    if issubclass(T, Bits):
        return T(init)
    elif issubclass(T, Array):
        return T([_zero_init(T.T, init) for _ in range(len(T))])
    elif issubclass(T, Tuple):
        return T(*(_zero_init(t, init) for t in T.types()))
    return T(init)


def _get_T_from_init(init):
    if isinstance(init, (bool, ht.Bit)):
        return Bit
    if isinstance(init, int):
        return Bits[max(init.bit_length(), 1)]
    if isinstance(init, ht.UIntVector):
        return UInt[len(init)]
    if isinstance(init, ht.SIntVector):
        return SInt[len(init)]
    if isinstance(init, ht.BitVector):
        return Bits[len(init)]
    if isinstance(init, Type):
        return type(init)
    raise ValueError(f"Could not infer register type from {init}")


def _check_init_T(init, T):
    init_T = _get_T_from_init(init)
    if isinstance(init, int) and issubclass(T, Bits):
        # Allow int to be extended to width of T
        if len(init_T) > len(T):
            # Don't implicitly truncate
            return False
        return True
    if isinstance(init, int) and issubclass(T, Bit):
        # Allow int for bit
        if len(init_T) > 1:
            return False
        return True
    return init_T.is_wireable(T)


class Register(Generator2):
    def __init__(self, T: Kind = None,
                 init: Union[Type, int, ht.BitVector] = None,
                 reset_type: AbstractReset = None, has_enable: bool = False,
                 reset_priority: bool = True, name_map=ParamDict(I="I",
                                                                 O="O",
                                                                 CE="CE")):
        """
        T: The type of the value that is stored inside the register (e.g.
           Bits[5])

        init: (optional) A const value (i.e. init.const() == True) of type T or
              an int to be used as the initial value of the register.
              If no value is provided, the register will be initialized with 0

        has_enable: (optional) whether the register has an enable signal

        reset_type: (optional) The type of the reset port (also specifies the
                    semantic behavior of the reset signal)

        reset_priority: (optional) boolean flag choosing whether synchronous
                        reset (RESET or RESETN) has priority over enable

        name_map: (optional) ParamDict mapping default port names to new names
        """
        if T is None:
            if init is None:
                raise ValueError("User must provide type T or init value (from"
                                 " which T will be inferred)")
            T = _get_T_from_init(init)
        else:
            if not isinstance(T, Kind):
                raise TypeError(
                    f"Expected instance of Kind for argument T, not {type(T)}")
            if init is not None and not _check_init_T(init, T):
                raise ValueError(
                    f"Type {_get_T_from_init(init)} of init ({init}) does not "
                    f"match T ({T})"
                )

        (
            has_async_reset, has_async_resetn, has_reset, has_resetn
        ) = get_reset_args(reset_type)

        I_name = name_map.get("I", "I")
        O_name = name_map.get("O", "O")
        CE_name = name_map.get("CE", "CE")
        self.io = IO(**{I_name: In(T), O_name: Out(T)})
        if has_enable:
            self.io += IO(**{CE_name: In(Enable)})
        self.io += ClockIO(has_async_reset=has_async_reset,
                           has_async_resetn=has_async_resetn,
                           has_reset=has_reset,
                           has_resetn=has_resetn)
        if init is None:
            init = 0

        if isinstance(init, int):
            init = _zero_init(T, init)

        self.init = init
        self.reset_type = reset_type

        coreir_init = init
        if isinstance(coreir_init, Type):
            coreir_init = as_bits(init)
        coreir_init = int(coreir_init)

        reg = _CoreIRRegister(T.flat_length(), init=coreir_init,
                              has_async_reset=has_async_reset,
                              has_async_resetn=has_async_resetn)()
        O = from_bits(T, reg.O)
        wire(O, getattr(self.io, O_name))

        I = getattr(self.io, I_name)
        if has_reset:
            reset_select = bit(self.io.RESET)
        elif has_resetn:
            reset_select = ~bit(self.io.RESETN)
        if has_enable:
            enable = getattr(self.io, CE_name)
        if (has_reset or has_resetn) and has_enable:
            if reset_priority:
                I = Mux(2, T)(name="enable_mux")(O, I, enable)
                I = Mux(2, T)()(I, init, reset_select)
            else:
                I = Mux(2, T)()(I, init, reset_select)
                I = Mux(2, T)(name="enable_mux")(O, I, enable)
        elif has_enable:
            I = Mux(2, T)(name="enable_mux")(O, I, enable)
        elif (has_reset or has_resetn):
            I = Mux(2, T)()(I, init, reset_select)
        reg.I @= as_bits(I)


def register(value, **kwargs):
    T = type(value).qualify(Direction.Undirected)
    inst_kwargs = {}
    try:
        name = kwargs.pop("name")
        inst_kwargs["name"] = name
    except KeyError:
        pass
    ckt = Register(T, **kwargs)
    return ckt(**inst_kwargs)(value)
