from magma.bit import Bit
from magma.bits import Bits
from magma.circuit import coreir_port_mapping
from magma.clock import AsyncReset, AsyncResetN, Clock, _ClockType
from magma.conversions import bit, convertbit
from magma.digital import Digital
from magma.generator import Generator2
from magma.interface import IO
from magma.t import In, Out


def _simulate_wire(self, value_store, state_store):
    value_store.set_value(self.O, value_store.get_value(self.I))


class Wire(Generator2):
    def __init__(self, T):
        if issubclass(T, (AsyncReset, AsyncResetN, Clock)):
            self._gen_named_type_wrapper(T)
            # Standalone return to avoid return-in-init lint warning
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

    def _gen_named_type_wrapper(self, T):
        """
        Generates a container around Wire(Bit) so named types are wrapped
        properly
        """
        assert issubclass(T, Digital)
        self.io = IO(I=In(T), O=Out(T))
        self.name = f"Wire{T}"
        self.io.O @= convertbit(Wire(Bit)()(bit(self.io.I)), T)
