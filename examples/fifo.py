import magma as m
import mantle


def make_Float(exponent_width, significand_width):
    # Adapted from the chisel documentation
    # https://github.com/freechipsproject/chisel3/wiki/Bundles-and-Vecs
    return m.Tuple(
        sign=m.Bit,
        exponent=m.UInt[exponent_width],
        significand=m.UInt[significand_width]
    )


def make_HandshakeData(data_type):
    in_type = m.Tuple(
        data=m.In(data_type),
        valid=m.In(m.Bit),
        ready=m.Out(m.Bit)
    )
    out_type = m.Flip(in_type)
    return in_type, out_type


def flat_length(tuple_):
    # Take a tuple type and return the width in bits when flattened
    # (for storage in a RAM)
    assert isinstance(tuple_, m.TupleType)

    flat_data_length = 0
    for value in tuple_.values():
        # Bits do not have a length (i.e. len(v) doesn't work when v is Bit),
        # to guard against cases when the user thinks a Bits[1] is equivalent
        # to a Bit, instead we count the Bit explicitly
        if isinstance(value, m.BitType):
            flat_data_length += 1
        else:
            flat_data_length += len(value)
    return flat_data_length


def flatten_fields_to_bits(tuple_):
    # Take a tuple and flatten it into a Bits representation so it can be used
    # in a RAM
    assert isinstance(tuple_, m.TupleType)
    fields = []
    for value in tuple_:
        # Promote Bit to Bits so we can concat
        if isinstance(value, m.BitType):
            value = m.bits(value, 1)
        fields.append(value)
    return m.concat(*fields)


def unflatten_bits_to_fields(tuple_, bits_):
    # Take raw bits and unpack them into tuple fields
    # (to read data from RAM into tuple)
    assert isinstance(tuple_, m.TupleType)
    fields = {}
    offset = 0
    # unpack bits into data
    for key in tuple_.keys():
        value = tuple_[key]
        if isinstance(value, m.BitType):
            fields[key] = bits_[offset]
            offset += 1
        else:
            fields[key] = bits_[offset:offset + len(value)]
            offset += len(value)
    return m.namedtuple(**fields)


def make_FIFO(data_in_type, data_out_type, depth):
    class FIFO(m.Circuit):
        io = m.IO(data_in=data_in_type, data_out=data_out_type)
        IO += m.ClockInterface()

        @classmethod
        def definition(io):
            addr_width = m.bitutils.clog2(depth)

            buffer = mantle.RAM(addr_width, flat_length(io.data_in.data))

            # pack data into bits
            buffer.WDATA <= flatten_fields_to_bits(io.data_in.data)

            # unpack bits into tuple
            io.data_out.data <= unflatten_bits_to_fields(io.data_out.data,
                                                         buffer.RDATA)

            read_pointer = mantle.Register(addr_width + 1)
            write_pointer = mantle.Register(addr_width + 1)
            buffer.RADDR <= read_pointer.O[:addr_width]
            buffer.WADDR <= write_pointer.O[:addr_width]

            full = \
                (read_pointer.O[:addr_width] == write_pointer.O[:addr_width]) \
                & \
                (read_pointer.O[addr_width] != write_pointer.O[addr_width])

            empty = read_pointer == write_pointer
            write_valid = io.data_in.valid & ~full
            read_valid = io.data_out.ready & ~empty

            io.data_in.ready <= ~full

            buffer.WE <= write_valid
            write_pointer.I <= mantle.mux([
                write_pointer.O, m.uint(write_pointer.O) + 1
            ], write_valid)

            io.data_out.valid <= read_valid

            read_pointer.I <= mantle.mux([
                read_pointer.O, m.uint(read_pointer.O) + 1
            ], read_valid)
    return FIFO


HSFloatIn, HSFloatOut = make_HandshakeData(make_Float(8, 23))
FIFO = make_FIFO(HSFloatIn, HSFloatOut, 4)

m.compile("examples/build/FIFO", FIFO, output="coreir-verilog")
