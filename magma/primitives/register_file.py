from ..generator import Generator
from ..circuit import Circuit, StagedCircuit, coreir_port_mapping
from ..t import In, Out
from ..interface import IO
from ..bits import Bits
from ..clock import ClockIO, Clock, AsyncResetIn, AsyncResetIn
from ..bitutils import clog2
from ..operators import Mux
from ..wire import wire
from ..tuple import Product
from ..ref import InstRef
from hwtypes import BitVector
import coreir


class CoreIRRegister(Generator):
    @staticmethod
    def generate(width, init=0, has_async_reset=False,
                 has_async_resetn=False):
        circuit_name = "reg_P"
        config_args = {"init": coreir.type.BitVector[width](init)}
        T = Bits[width]
        io = ["I", In(T), "CLK", In(Clock), "O", Out(T)]

        if has_async_resetn and has_async_reset:
            raise ValueError("Cannot have posedge and negedge asynchronous "
                             "reset")

        if has_async_reset:
            io.extend(["arst", In(AsyncResetIn)])
            circuit_name += "R"
            config_args["arst_posedge"] = True

        if has_async_resetn:
            io.extend(["arst", In(AsyncResetNIn)])
            circuit_name += "R"
            config_args["arst_posedge"] = False

        io_dict = {}
        for key, value in zip(io[::2], io[1::2]):
            io_dict[key] = value

        class _CoreIRReg(Circuit):
            name = circuit_name
            io = IO(**io_dict)
            stateful = True
            default_kwargs = {"init": coreir.type.BitVector[width](init)}
            coreir_genargs = {"width": width}
            coreir_configargs = config_args
            renamed_ports = coreir_port_mapping

            if (has_async_reset or has_async_resetn):
                coreir_name = "reg_arst"
            else:
                coreir_name = "reg"

            verilog_name = "coreir_" + coreir_name
            coreir_lib = "coreir"

            def simulate(self, value_store, state_store):
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

                if has_async_reset and cur_reset or \
                        has_async_resetn and not cur_reset:
                    new_val = BitVector[width](init)

                state_store['prev_clock'] = cur_clock
                state_store['cur_val'] = BitVector[width](new_val)
                value_store.set_value(self.O, new_val)
        return _CoreIRReg


class RegisterFile(Generator):
    """
    Generate a height by width register file with an arbitrary number of
    read/write ports.

    Using the __getitem__ operator adds a new read port
    Using the __setitem__ operator adds a new write port

    Reading and writing use combinational semantics (a read after write of the
    same address will read the newly written value)

    TODO: We should optimize cases where a written value is never read, so it
    doesn't need the write forwarding mux, but by default we can generate it.

    This implements the Pythonic semantics (blocking assignemnts), do we want
    to have a non-blocking mode? (e.g. write have a one cycle delay).
    """
    # Naive implementation, create a unique circuit for every instance (since
    # each circuit will be editing it's type)
    cache = False

    @staticmethod
    def generate(height: int, width: int):
        data_width = width
        addr_width = clog2(height)

        class ReadPortT(Product):
            data = Out(Bits[data_width])
            addr = In(Bits[addr_width])

        class WritePortT(Product):
            data = In(Bits[data_width])
            addr = In(Bits[addr_width])

        class _RegisterFile(StagedCircuit):
            # We start with just a clock, ports are added in stages
            io = ClockIO(has_async_reset=True)
            registers = [CoreIRRegister(width, has_async_reset=True) for _ in
                         range(height)]

            num_read_ports = 0
            num_write_ports = 0

            def _add_port(self, name, type_):
                cls = type(self)
                # Add to Circuit IO
                curr_IO = IO(
                    **{key: value for key, value in cls.IO.items()}
                )
                cls.io += curr_IO + IO(**{name: type_})
                del cls.IO
                cls.setup_interface()
                # Add to instance interface
                value = type_(name=InstRef(self, name))
                self.interface.ports[name] = value
                setattr(self, name, value)
                return value

            def __getitem__(self, addr):
                """
                Add a read port
                """
                cls = type(self)
                read_port = self._add_port(f"read_{cls.num_read_ports}",
                                           ReadPortT)
                cls.num_read_ports += 1
                wire(addr, read_port.addr)
                return read_port.data

            def __setitem__(self, addr, data):
                """
                Add a write port
                """
                cls = type(self)
                write_port = self._add_port(f"write_{cls.num_write_ports}",
                                            WritePortT)
                cls.num_write_ports += 1
                wire(addr, write_port.addr)
                wire(data, write_port.data)

            @classmethod
            def _get_read_ports(cls):
                return filter(lambda port: isinstance(port, ReadPortT.flip()),
                              cls.interface.ports.values())

            @classmethod
            def _get_write_ports(cls):
                return filter(lambda port: isinstance(port, WritePortT.flip()),
                              cls.interface.ports.values())

            @classmethod
            def finalize(cls):
                with cls.open():
                    for port in cls._get_read_ports():
                        port.data @= Mux(height, Bits[data_width])(
                            *[register.O for register in cls.registers],
                            port.addr)
                    for port in cls._get_write_ports():
                        for i, register in enumerate(cls.registers):
                            if register.I.driven():
                                value = register.I.value()
                                register.I.unwire(value)
                            else:
                                value = register.O
                            register.I @= Mux(2, Bits[data_width])(
                                value, port.data,
                                Bits[1](port.addr == i))
                        for read_port in cls._get_read_ports():
                            # Forward write
                            value = read_port.data.value()
                            read_port.data.unwire(value)
                            read_port.data @= Mux(
                                2, Bits[data_width])(
                                    value, port.data,
                                    Bits[1](port.addr == read_port.addr))
        return _RegisterFile
