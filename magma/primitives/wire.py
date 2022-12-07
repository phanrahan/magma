from magma.bit import Bit
from magma.bits import Bits
from magma.circuit import coreir_port_mapping
from magma.clock import AsyncReset, AsyncResetN, Clock, _ClockType
from magma.conversions import bit, convertbit
from magma.digital import Digital
from magma.generator import Generator2
from magma.interface import IO
from magma.t import Kind, In, Out
from magma.type_utils import type_to_sanitized_string


def _simulate_wire(this, value_store, state_store):
    value_store.set_value(this.O, value_store.get_value(this.I))


class Wire(Generator2):
    def __init__(self, T: Kind, flatten: bool = True):
        self.T = T
        self.flattened = flatten
        if not flatten:
            self._init_unflattened(T)
            return
        if issubclass(T, (AsyncReset, AsyncResetN, Clock)):
            self._init_named_type_wrapper(T)
            return
        if issubclass(T, Digital):
            coreir_lib = "corebit"
            coreir_genargs = None
        else:
            width = T.flat_length()
            T = Bits[width]
            coreir_lib = "coreir"
            coreir_genargs = {"width": width}
        self.name = "Wire"
        self.io = IO(I=In(T), O=Out(T))
        self.simulate = _simulate_wire
        self.coreir_name = "wire"
        self.coreir_lib = coreir_lib
        self.coreir_genargs = coreir_genargs
        self.renamed_ports = coreir_port_mapping
        self.primitive = True

    def _init_unflattened(self, T: Kind):
        self.name = f"Wire{type_to_sanitized_string(T)}"
        self.io = IO(I=In(T), O=Out(T))
        self.simulate = _simulate_wire
        self.primitive = True

    def _init_named_type_wrapper(self, T: Kind):
        """Generates a container around Wire(Bit) so named types are wrapped
        properly.
        """
        assert issubclass(T, Digital)
        self.io = IO(I=In(T), O=Out(T))
        self.name = f"Wire{T}"
        self.io.O @= convertbit(Wire(Bit)()(bit(self.io.I)), T)
