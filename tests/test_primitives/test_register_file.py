import magma as m
from magma.primitives.register_file import RegisterFile
from magma.testing import check_files_equal


def test_register_file_primitive_basic():
    height = 4
    data_width = 4
    addr_width = m.bitutils.clog2(height)

    class Main(m.Circuit):
        io = m.IO(
            write_addr=m.In(m.Bits[addr_width]),
            write_data=m.In(m.Bits[data_width]),
            read_addr=m.In(m.Bits[addr_width]),
            read_data=m.Out(m.Bits[data_width])
        ) + m.ClockIO(has_async_reset=True)
        reg_file = RegisterFile(height, data_width)
        # TODO: Perhaps we can support imatmal with getitem to keep
        # consistency?
        reg_file[io.write_addr] = io.write_data
        io.read_data @= reg_file[io.read_addr]

    m.compile("build/test_register_file_primitive_basic", Main, inline=True)
    assert check_files_equal(__file__,
                             "build/test_register_file_primitive_basic.v",
                             "gold/test_register_file_primitive_basic.v")
