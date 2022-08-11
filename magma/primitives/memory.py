from typing import Optional
from hwtypes import BitVector

from magma.bits import Bits
from magma.bitutils import clog2
from magma.clock import Clock, Enable
from magma.clock_io import ClockIO
from magma.conversions import from_bits, as_bits, enable, uint
from magma.generator import Generator2
from magma.interface import IO
from magma.logging import root_logger
from magma.passes import DefinitionPass, pass_lambda
from magma.primitives.register import Register
from magma.primitives.when import When
from magma.protocol_type import MagmaProtocol, MagmaProtocolMeta
from magma.t import In, Out, Kind, Type
from magma.when import finalize as finalize_when_block


_logger = root_logger()


class CoreIRMemory(Generator2):
    def __init__(self, depth, width, init=None, sync_read=False):
        self.name = f"coreir_mem{depth}x{width}"
        addr_width = clog2(depth)
        self.io = IO(
            raddr=In(Bits[addr_width]),
            rdata=Out(Bits[width]),
            waddr=In(Bits[addr_width]),
            wdata=In(Bits[width]),
            clk=In(Clock),
            wen=In(Enable)
        )
        self.verilog_name = "coreir_mem"
        if sync_read:
            self.io += IO(ren=In(Enable))
            self.coreir_name = "sync_read_mem"
            self.coreir_lib = "memory"
        else:
            self.coreir_name = "mem"
            self.coreir_lib = "coreir"
        self.coreir_genargs = {"width": width, "depth": depth,
                               "has_init": init is not None}
        self.coreir_configargs = {}
        if init is not None:
            self.coreir_configargs["init"] = [
                int(uint(as_bits(x))) if isinstance(x, Type)
                else int(x) for x in init
            ]

        def _simulate(self, value_store, state_store):
            cur_clk = value_store.get_value(self.clk)

            if not state_store:
                state_store['mem'] = [
                    BitVector[width](0) for _ in range(depth)
                ]
                state_store['prev_clk'] = cur_clk

            prev_clk = state_store['prev_clk']
            clk_edge = cur_clk and not prev_clk
            rdata = value_store.get_value(self.rdata)

            if clk_edge:
                index = int(
                    BitVector[addr_width](value_store.get_value(self.raddr))
                )
                rdata = state_store['mem'][index].as_bool_list()

            if clk_edge:
                if value_store.get_value(self.wen):
                    index = int(
                        BitVector[addr_width](value_store.get_value(self.waddr))
                    )
                    state_store['mem'][index] = BitVector[width](
                        value_store.get_value(self.wdata)
                    )

            state_store['prev_clk'] = cur_clk
            value_store.set_value(self.rdata, rdata)

        self.simulate = _simulate
        self.primitive = True
        self.stateful = True


class StagedMemoryPortMeta(MagmaProtocolMeta):
    def _to_magma_(cls):
        return cls.T

    def _qualify_magma_(cls, direction):
        return cls[cls.T.qualify(direction)]

    def _flip_magma_(cls):
        return cls[cls.T.flip()]

    def _from_magma_value_(cls, val):
        return value

    def __getitem__(cls, T):
        return type(cls)(f"StagedMemoryPort{T}", (cls, ), {"T": T})


class StagedMemoryPort(MagmaProtocol, metaclass=StagedMemoryPortMeta):
    def __init__(self, memory, addr):
        self.memory = memory
        self.addr = addr

    def __imatmul__(self, data):
        self.memory.WADDR @= self.addr
        self.memory.WDATA @= data
        self.memory.WE @= 1
        return self

    def _get_magma_value_(self):
        self.memory.RADDR @= self.addr
        return self.memory.RDATA


class Memory(Generator2):
    def __init__(self, height, T: Kind,
                 read_latency: int = 0, read_only: bool = False,
                 init: Optional[tuple] = None, has_read_enable: bool = False):
        if read_latency < 0:
            raise ValueError("read_latency cannot be negative")
        if has_read_enable and read_latency == 0:
            raise ValueError(
                "Can only use has_read_enable with read_latency >= 1")
        addr_width = clog2(height)
        data_width = T.flat_length()
        # For ROM, we use coreir's generic mem and tie off the write signals
        self.io = IO(
            RADDR=In(Bits[addr_width]),
            RDATA=Out(T),
        ) + ClockIO()
        if has_read_enable:
            self.io += IO(RE=In(Enable))
        if not read_only:
            self.io += IO(
                WADDR=In(Bits[addr_width]),
                WDATA=In(T),
                WE=In(Enable)
            )
            waddr = self.io.WADDR
            wdata = as_bits(self.io.WDATA)
            wen = self.io.WE
        else:
            waddr = Bits[addr_width](0)
            wdata = Bits[data_width](0)
            wen = Enable(0)
        coreir_mem = CoreIRMemory(height, data_width, init=init,
                                  sync_read=read_latency > 0)()
        coreir_mem.waddr @= waddr
        coreir_mem.wdata @= wdata
        coreir_mem.wen @= wen
        coreir_mem.raddr @= self.io.RADDR
        rdata = from_bits(T, coreir_mem.rdata)
        if read_latency > 0:
            RE = enable(1) if not has_read_enable else self.io.RE
            coreir_mem.ren @= RE
            # -1 because sync_read param handles latency 1
            for _ in range(read_latency - 1):
                rdata = Register(T, has_enable=True)()(rdata, CE=RE)
        self.io.RDATA @= rdata

        def __setitem__(self, key, value):
            if not isinstance(value, StagedMemoryPort):
                raise TypeError("Cannot call __setitem__ directly on memory"
                                "instance")
            assert key is value.addr
            assert value.memory is self

        self.__setitem__ = __setitem__

        def __getitem__(self, addr):
            return StagedMemoryPort[T](self, addr)

        self.__getitem__ = __getitem__

        if has_read_enable:
            def read(self, addr, ren):
                self.RADDR @= addr
                self.RE @= ren
                return self.RDATA
        else:
            def read(self, addr):
                self.RADDR @= addr
                return self.RDATA

        self.read = read

        if not read_only:
            def write(self, data, addr, when):
                self.WDATA @= data
                self.WADDR @= addr
                self.WE @= when
            self.write = write

        self._is_magma_memory_ = True


def _get_memory_port_drivee(value: Type) -> Optional[Type]:
    drivee = value.value()
    assert drivee is not None
    root_ref = drivee.name.root()
    try:
        drivee_inst = root_ref.inst
    except AttributeError:
        return None
    if not isinstance(type(drivee_inst), Memory):
        return None
    if root_ref.name not in ("WDATA", "WADDR", "WE", "RADDR"):
        return None
    return drivee


def _add_default_drivers_to_memory_ports(containing_defn, when_inst):
    assert isinstance(type(when_inst), When)
    modified = False
    for port in when_inst.interface.outputs():
        drivee = _get_memory_port_drivee(port)
        if drivee is None:
            continue
        modified = True
        T = type(drivee).undirected_t
        zero = from_bits(T, Bits[T.flat_length()](0))
        type(when_inst).block.add_default_driver(drivee, zero)
    if not modified:
        return
    with containing_defn.open():
        for port in when_inst.interface.outputs():
            port.value().unwire(port)
        for port in when_inst.interface.inputs():
            port.unwire(port.value())
        containing_defn._context_.placer._instances.remove(when_inst)
        finalize_when_block(type(when_inst).block)


class AddWhenDefaultDriversToMemory(DefinitionPass):
    def __call__(self, defn):
        if not any(isinstance(type(inst), Memory) for inst in defn.instances):
            return
        for inst in defn.instances:
            if not isinstance(type(inst), When):
                continue
            _add_default_drivers_to_memory_ports(defn, inst)


add_when_default_drivers_to_memory = pass_lambda(AddWhenDefaultDriversToMemory)
