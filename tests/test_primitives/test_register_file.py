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
    try:
        import fault
        import tempfile
        tester = fault.Tester(Main, Main.CLK)
        tester.circuit.CLK = 0
        for i in range(4):
            tester.circuit.write_addr = i
            tester.circuit.write_data = i
            tester.step(2)
        for i in range(4):
            tester.circuit.read_addr = i
            tester.eval()
            tester.circuit.read_data.expect(i)
        with tempfile.TemporaryDirectory() as dir_:
            tester.compile_and_run("verilator", directory=dir_, flags=['-Wno-unused'])
    except ImportError:
        pass


def test_register_file_primitive_two():
    height = 4
    data_width = 4
    addr_width = m.bitutils.clog2(height)

    class Main(m.Circuit):
        io = m.IO(
            write_addr0=m.In(m.Bits[addr_width]),
            write_data0=m.In(m.Bits[data_width]),
            write_addr1=m.In(m.Bits[addr_width]),
            write_data1=m.In(m.Bits[data_width]),
            read_addr0=m.In(m.Bits[addr_width]),
            read_data0=m.Out(m.Bits[data_width]),
            read_addr1=m.In(m.Bits[addr_width]),
            read_data1=m.Out(m.Bits[data_width])
        ) + m.ClockIO(has_async_reset=True)
        reg_file = RegisterFile(height, data_width)
        # TODO: Perhaps we can support imatmal with getitem to keep
        # consistency?
        reg_file[io.write_addr0] = io.write_data0
        io.read_data0 @= reg_file[io.read_addr0]
        reg_file[io.write_addr1] = io.write_data1
        io.read_data1 @= reg_file[io.read_addr1]

    m.compile("build/test_register_file_primitive_two", Main, inline=True)
    assert check_files_equal(__file__,
                             "build/test_register_file_primitive_two.v",
                             "gold/test_register_file_primitive_two.v")
    try:
        import fault
        import tempfile
        tester = fault.Tester(Main, Main.CLK)
        tester.circuit.CLK = 0
        for i in range(4):
            tester.circuit.write_addr0 = i
            tester.circuit.write_data0 = 3 - i
            tester.circuit.write_addr1 = 3 - i
            tester.circuit.write_data1 = i
            tester.step(2)
        for i in range(4):
            tester.circuit.read_addr0 = i
            tester.circuit.read_addr1 = 3 - i
            tester.eval()
            if i == 0:
                tester.circuit.read_data0.expect(3 - i)
                tester.circuit.read_data1.expect(i)
            elif i == 1:
                tester.circuit.read_data0.expect(3 - i)
                tester.circuit.read_data1.expect(i)
            elif i == 2:
                tester.circuit.read_data0.expect(3 - i)
                tester.circuit.read_data1.expect(i)
            elif i == 3:
                tester.circuit.read_data0.expect(3 - i)
                tester.circuit.read_data1.expect(i)

        # Test priority
        tester.circuit.write_addr0 = 3
        tester.circuit.write_data0 = 3
        tester.circuit.write_addr1 = 3
        tester.circuit.write_data1 = 4
        tester.step(2)
        tester.circuit.read_addr0 = 3
        tester.eval()
        tester.circuit.read_data0.expect(4)
        with tempfile.TemporaryDirectory() as dir_:
            tester.compile_and_run("verilator", directory=dir_, flags=['-Wno-unused'])
    except ImportError:
        pass
