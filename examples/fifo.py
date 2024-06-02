import magma as m


def make_Float(exponent_width, significand_width):
    class Float(m.Product):
        sign = m.Bit
        exponent = m.UInt[exponent_width]
        significand = m.UInt[significand_width]
    return Float


class FIFO(m.Generator):
    def __init__(self, T, depth):
        self.io = m.IO(data_in=m.Consumer(m.ReadyValid[T]),
                       data_out=m.Producer(m.ReadyValid[T]))
        self.io += m.ClockIO()

        addr_width = m.bitutils.clog2(depth)

        buffer = m.Memory(2**addr_width, T)()

        buffer.WDATA @= self.io.data_in.data
        self.io.data_out.data @= buffer.RDATA

        read_pointer = m.Register(m.Bits[addr_width + 1])()
        write_pointer = m.Register(m.Bits[addr_width + 1])()
        buffer.RADDR @= read_pointer.O[:addr_width]
        buffer.WADDR @= write_pointer.O[:addr_width]

        full = \
            (read_pointer.O[:addr_width] == write_pointer.O[:addr_width]) \
            & \
            (read_pointer.O[addr_width] != write_pointer.O[addr_width])

        empty = read_pointer == write_pointer
        write_valid = self.io.data_in.valid & ~full
        read_valid = self.io.data_out.ready & ~empty

        self.io.data_in.ready @= ~full

        buffer.WE @= write_valid
        write_pointer.I @= m.mux([
            write_pointer.O, m.uint(write_pointer.O) + 1
        ], write_valid)

        self.io.data_out.valid @= read_valid

        read_pointer.I @= m.mux([
            read_pointer.O, m.uint(read_pointer.O) + 1
        ], read_valid)

m.compile("build/FIFO", FIFO(make_Float(8, 23), 4), output="mlir-verilog")
