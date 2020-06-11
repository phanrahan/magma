import magma as m
import mantle


def make_Float(exponent_width, significand_width):
    # Adapted from the chisel documentation
    # https://github.com/freechipsproject/chisel3/wiki/Bundles-and-Vecs
    return m.Product.from_fields("Float", {
        "sign": m.Bit,
        "exponent": m.UInt[exponent_width],
        "significand": m.UInt[significand_width]
    })


def make_HandshakeData(data_type):
    in_type = m.Product.from_fields("HandshakeData", {
        "data": m.In(data_type),
        "valid": m.In(m.Bit),
        "ready": m.Out(m.Bit)
    })
    out_type = m.Flip(in_type)
    return in_type, out_type


def make_FIFO(data_in_type, data_out_type, depth):
    class FIFO(m.Circuit):
        io = m.IO(data_in=data_in_type, data_out=data_out_type)
        io += m.ClockIO()

        addr_width = m.bitutils.clog2(depth)

        buffer = mantle.RAM(2**addr_width, io.data_in.data.flat_length())

        # pack data into bits
        buffer.WDATA @= m.as_bits(io.data_in.data)

        # unpack bits into tuple
        io.data_out.data @= m.from_bits(data_out_type.data, buffer.RDATA)

        read_pointer = mantle.Register(addr_width + 1)
        write_pointer = mantle.Register(addr_width + 1)
        buffer.RADDR @= read_pointer.O[:addr_width]
        buffer.WADDR @= write_pointer.O[:addr_width]

        full = \
            (read_pointer.O[:addr_width] == write_pointer.O[:addr_width]) \
            & \
            (read_pointer.O[addr_width] != write_pointer.O[addr_width])

        empty = read_pointer == write_pointer
        write_valid = io.data_in.valid & ~full
        read_valid = io.data_out.ready & ~empty

        io.data_in.ready @= ~full

        buffer.WE @= write_valid
        write_pointer.I @= mantle.mux([
            write_pointer.O, m.uint(write_pointer.O) + 1
        ], write_valid)

        io.data_out.valid @= read_valid

        read_pointer.I @= mantle.mux([
            read_pointer.O, m.uint(read_pointer.O) + 1
        ], read_valid)
    return FIFO


HSFloatIn, HSFloatOut = make_HandshakeData(make_Float(8, 23))
FIFO = make_FIFO(HSFloatIn, HSFloatOut, 4)

m.compile("examples/build/FIFO", FIFO, output="coreir-verilog")
