from typing import Union

import coreir
import hwtypes

from magma.array import Array
from magma.bit import Bit
from magma.bits import Bits
from magma.circuit import coreir_port_mapping
from magma.conversions import as_bits, from_bits
from magma.interface import IO
from magma.generator import Generator2
from magma.t import Type, Kind, In, Out
from magma.tuple import Tuple
from magma.clock import (AbstractReset,
                         AsyncReset, AsyncResetN, Clock, get_reset_args)
from magma.clock_io import ClockIO
from magma.primitives.mux import Mux


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
            self.name += "R"
            self.coreir_configargs["arst_posedge"] = False

        self.stateful = True
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
                state_store['cur_val'] = hwtypes.BitVector[width](init)

            if has_async_reset or has_async_resetn:
                cur_reset = value_store.get_value(self.arst)

            prev_clock = state_store['prev_clock']
            clock_edge = cur_clock and not prev_clock

            new_val = state_store['cur_val'].as_bool_list()

            if clock_edge:
                new_val = value_store.get_value(self.I)

            if has_async_reset and cur_reset or \
                    has_async_resetn and not cur_reset:
                new_val = hwtypes.BitVector[width](init)

            state_store['prev_clock'] = cur_clock
            state_store['cur_val'] = hwtypes.BitVector[width](new_val)
            value_store.set_value(self.O, new_val)
        self.simulate = _simulate


def _zero_init(T, init):
    if issubclass(T, Array):
        return T([_zero_init(T.T, init) for _ in range(len(T))])
    elif issubclass(T, Tuple):
        return T(*(_zero_init(t, init) for t in T.types()))
    return T(init)


class Register(Generator2):
    def __init__(self, T: Kind, init: Union[Type, int] = None, reset_type:
                 AbstractReset = None, has_enable: bool = False,
                 reset_priority=True):
        """
        T: The type of the value that is stored inside the register (e.g.
           Bits[5])

        init: (optional) A const value (i.e. init.const() == True) of type T or
              an int to be used as the initial value of the register.
              If no value is provided, the register will be initialized with 0

        reset_type: (optional) The type of the reset port (also specifies the
                    semantic behavior of the reset signal)

        reset_priority: (optional) boolean flag choosing whether synchronous
                        reset (RESET or RESETN) has priority over enable
        """
        if not isinstance(T, Kind):
            raise TypeError(
                f"Expected instance of Kind for argument T, not {type(T)}")
        if init is not None and not isinstance(init, (Type, int)):
            raise TypeError(
                f"Expected instance of Type or int for argument init, not "
                f"{type(init)}")
        (
            has_async_reset, has_async_resetn, has_reset, has_resetn
        ) = get_reset_args(reset_type)

        self.io = IO(I=In(T), O=Out(T))
        self.io += ClockIO(has_enable=has_enable,
                           has_async_reset=has_async_reset,
                           has_async_resetn=has_async_resetn,
                           has_reset=has_reset,
                           has_resetn=has_resetn)
        if init is None:
            init = 0

        if isinstance(init, int):
            init = _zero_init(T, init)

        if has_async_reset or has_async_resetn:
            coreir_init = int(as_bits(init))
        else:
            coreir_init = 0

        reg = _CoreIRRegister(T.flat_length(), init=coreir_init,
                              has_async_reset=has_async_reset,
                              has_async_resetn=has_async_resetn)()
        O = from_bits(T, reg.O)
        self.io.O @= O

        I = self.io.I
        if has_reset:
            reset_port = self.io.RESET
        elif has_resetn:
            reset_port = self.io.RESETN
        if (has_reset or has_resetn) and has_enable:
            if reset_priority:
                I = Mux(2, T)(name="enable_mux")(O, I, self.io.CE)
                I = Mux(2, T)()(I, init, reset_port)
            else:
                I = Mux(2, T)()(I, init, reset_port)
                I = Mux(2, T)(name="enable_mux")(O, I, self.io.CE)
        elif has_enable:
            I = Mux(2, T)(name="enable_mux")(O, I, self.io.CE)
        elif (has_reset or has_resetn):
            I = Mux(2, T)()(I, init, reset_port)
        reg.I @= as_bits(I)
