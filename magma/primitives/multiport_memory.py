from magma.bits import Bits
from magma.bitutils import clog2
from magma.clock import Enable
from magma.clock_io import ClockIO
from magma.generator import Generator2
from magma.interface import IO
from magma.t import In, Out, Kind


class MultiportMemory(Generator2):
    def __init__(
            self,
            height: int,
            T: Kind,
            num_read_ports: int = 1,
            num_write_ports: int = 1,
            has_read_enable: bool = False
    ):
        if num_read_ports < 1:
            raise ValueError("At least one read port is required")
        if num_write_ports < 0:
            raise ValueError("Number of write ports must be non-negative")

        self.num_read_ports = num_read_ports
        self.has_read_enable = has_read_enable
        self.num_write_ports = num_write_ports
        self.T = T
        self.height = height

        addr_width = clog2(height)

        self.io = ClockIO()
        for i in range(num_read_ports):
            self.io += IO(**{
                f"RADDR_{i}": In(Bits[addr_width]),
                f"RDATA_{i}": Out(T)
            })
            if has_read_enable:
                self.io += IO(**{f"RE_{i}": In(Enable)})
        for i in range(num_write_ports):
            self.io += IO(**{
                f"WADDR_{i}": In(Bits[addr_width]),
                f"WDATA_{i}": In(T),
                f"WE_{i}": In(Enable)
            })
        self.primitive = True
