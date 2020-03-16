from magma import Generator, Circuit, CircuitBuilder, In, Out, IO, Bits, Clock, AsyncResetIn, ClockIO, wire, Product, InstRef
from magma import Generator2
from magma import CircuitBuilder, builder_method
from magma import ClockInterface
from magma import bits
from magma.bitutils import clog2
from magma.circuit import coreir_port_mapping
from magma.operators import Mux
from hwtypes import BitVector
# from ..generator import Generator
# from ..circuit import Circuit, StagedCircuit, coreir_port_mapping
# from ..t import In, Out
# from ..interface import IO
# from ..bits import Bits
# from ..clock import Clock, AsyncResetIn, AsyncResetIn
# from ..clock_io import ClockIO
# from ..bitutils import clog2
# from ..operators import Mux
# from ..wire import wire
# from ..tuple import Product
# from ..ref import InstRef
from hwtypes import BitVector
import coreir


def _simulate_reg(self, value_store, state_store):
    cur_clock = value_store.get_value(self.CLK)
    if not state_store:
        state_store['prev_clock'] = cur_clock
        state_store['cur_val'] = BitVector[width](init)
    if has_async_reset or has_async_resetn:
        cur_reset = value_store.get_value(self.arst)
    prev_clock = state_store['prev_clock']
    clock_edge = cur_clock and not prev_clock
    new_val = state_store['cur_val'].as_bool_list()
    if clock_edge:
        new_val = value_store.get_value(self.I)
    if has_async_reset and cur_reset or has_async_resetn and not cur_reset:
        new_val = BitVector[width](init)
    state_store['prev_clock'] = cur_clock
    state_store['cur_val'] = BitVector[width](new_val)
    value_store.set_value(self.O, new_val)


def _make_read_type(data_width, addr_width):
    fields = dict(data=Out(Bits[data_width]), addr=In(Bits[addr_width]))
    return Product.from_fields("ReadPortT", fields)

def _make_write_type(data_width, addr_width):
    fields = dict(data=In(Bits[data_width]), addr=In(Bits[addr_width]))
    return Product.from_fields("WritePortT", fields)


class CoreIRRegister(Generator2):
    def __init__(self, width, init=0, has_async_reset=False,
                 has_async_resetn=False):
        name = "reg_P"
        config_args = {"init": coreir.type.BitVector[width](init)}
        T = Bits[width]
        io = {"I": In(T), "CLK": In(Clock), "O": Out(T)}

        if has_async_resetn and has_async_reset:
            raise ValueError("Cannot have posedge and negedge async. reset")

        if has_async_reset:
            io["arst"] = In(AsyncResetIn)
            name += "R"
            config_args["arst_posedge"] = True

        if has_async_resetn:
            io["arst"] = In(AsyncResetNIn)
            name += "R"
            config_args["arst_posedge"] = False

        self.name = name
        self.io = IO(**io)
        self.stateful = True
        self.default_kwargs = {"init": coreir.type.BitVector[width](init)}
        self.coreir_genargs = {"width": width}
        self.coreir_configargs = config_args
        self.renamed_ports = coreir_port_mapping
        if has_async_reset or has_async_resetn:
            self.coreir_name = "reg_arst"
        else:
            self.coreir_name = "reg"
        self.verilog_name = "coreir_" + self.coreir_name
        self.coreir_lib = "coreir"
        self.simulate = _simulate_reg


class RegisterFile(CircuitBuilder):
    def __init__(self, name, height: int, width: int):
        super().__init__(name)
        self._data_width = width
        self._height = height
        self._addr_width = clog2(height)
        self._read_ports = []
        self._write_ports = []
        self._readT = _make_read_type(self._data_width, self._addr_width)
        self._writeT = _make_write_type(self._data_width, self._addr_width)
        clocks = ClockInterface(has_async_reset=True)
        for name, typ in zip(clocks[::2], clocks[1::2]):
            self._add_port(name, typ)

    @builder_method
    def __getitem__(self, addr):
        """Add a read port"""
        count = len(self._read_ports)
        name = f"read_{count}"
        self._add_port(name, self._readT)
        self._read_ports.append(name)
        port = getattr(self, name)
        wire(addr, port.addr)
        return port.data

    @builder_method
    def __setitem__(self, addr, data):
        """Add a write port"""
        count = len(self._write_ports)
        name = f"write_{count}"
        self._add_port(name, self._writeT)
        self._write_ports.append(name)
        port = getattr(self, name)
        wire(addr, port.addr)
        wire(data, port.data)

    @builder_method
    def _finalize(self):
        registers = [CoreIRRegister(self._data_width, has_async_reset=True)()
                    for _ in range(self._height)]
        for name in self._read_ports:
            port = self._port(name)
            mux = Mux(self._height, Bits[self._data_width])()
            values = [reg.O for reg in registers]
            port.data @= mux(*values, port.addr)
        for name in self._write_ports:
            port = self._port(name)
            for i, reg in enumerate(registers):
                if reg.I.driven():
                   value = reg.I.value()
                   reg.I.unwire(value)
                else:
                   value = reg.O
                mux = Mux(2, Bits[self._data_width])()
                sel = bits(port.addr == i, 1)
                reg.I @= mux(reg.O, port.data, sel)
            for name in self._read_ports:  # forward write
                read_port = self._port(name)
                value = read_port.data.value()
                read_port.data.unwire(value)
                mux = Mux(2, Bits[self._data_width])()
                sel = Bits[1](port.addr == read_port.addr)
                read_port.data @= mux(value, port.data, sel)


def test_register_file_primitive_basic():
    import magma as m
    m.config.set_debug_mode(True)

    height = 4
    data_width = 4
    addr_width = m.bitutils.clog2(height)

    class _Main(m.Circuit):
        io = m.IO(
            write_addr=m.In(m.Bits[addr_width]),
            write_data=m.In(m.Bits[data_width]),
            read_addr=m.In(m.Bits[addr_width]),
            read_data=m.Out(m.Bits[data_width])
        ) + m.ClockIO(has_async_reset=True)
        reg_file = RegisterFile("my_regfile",  height, data_width)
        # TODO: Perhaps we can support imatmal with getitem to keep
        # consistency?
        reg_file[io.write_addr] = io.write_data
        io.read_data @= reg_file[io.read_addr]

    m.compile("regfile", _Main, inline=True)


if __name__ == "__main__":
    test_register_file_primitive_basic()
