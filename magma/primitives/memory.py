from typing import Optional
from hwtypes import BitVector

from magma.bit import Bit
from magma.bits import Bits
from magma.bitutils import clog2
from magma.clock import Clock, Enable
from magma.clock_io import ClockIO
from magma.conversions import from_bits, as_bits
from magma.generator import Generator2
from magma.interface import IO
from magma.primitives.register import Register
from magma.t import In, Out, Kind


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
        self.coreir_name = "mem"
        self.coreir_lib = "coreir"
        self.coreir_genargs = {"width": width, "depth": depth,
                               "has_init": init is not None,
                               "sync_read": sync_read}
        self.coreir_configargs = {}
        if init is not None:
            self.coreir_configargs["init"] = [int(x) for x in init]

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


class Memory(Generator2):
    def __init__(self, height, T: Kind,
                 read_latency: int = 0, read_only: bool = False,
                 init: Optional[tuple] = None):
        if read_latency < 0:
            raise ValueError("read_latency cannot be negative")
        addr_width = clog2(height)
        data_width = T.flat_length()
        # For ROM, we use coreir's generic mem and tie off the write signals
        self.io = IO(
            RADDR=In(Bits[addr_width]),
            RDATA=Out(T),
        ) + ClockIO()
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
            wen = Bit(0)
        coreir_mem = CoreIRMemory(height, data_width, init=init,
                                  sync_read=read_latency > 0)()
        coreir_mem.waddr @= waddr
        coreir_mem.wdata @= wdata
        coreir_mem.wen @= wen
        coreir_mem.raddr @= self.io.RADDR
        rdata = from_bits(T, coreir_mem.rdata)
        # -1 because sync_read param handles latency 1
        for _ in range(read_latency - 1):
            rdata = Register(T)()(rdata)
        self.io.RDATA @= rdata
