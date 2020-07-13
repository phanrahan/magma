import os

import magma as m
from magma.testing import check_files_equal
from magma.primitives import Register

import fault


def test_basic_reg():
    class test_basic_reg(m.Circuit):
        io = m.IO(I=m.In(m.Bits[8]), O=m.Out(m.Bits[8])) + m.ClockIO(has_reset=True)
        io.O @= Register(m.Bits[8], m.Bits[8](0xDE), reset_type=m.Reset)()(io.I)

    m.compile("build/test_basic_reg", test_basic_reg)

    assert check_files_equal(__file__, f"build/test_basic_reg.v",
                             f"gold/test_basic_reg.v")

    tester = fault.SynchronousTester(test_basic_reg, test_basic_reg.CLK)
    tester.circuit.I = 0
    tester.circuit.RESET = 1
    tester.advance_cycle()
    tester.circuit.RESET = 0
    # Reset val
    tester.circuit.O.expect(0xDE)
    tester.advance_cycle()
    tester.circuit.O.expect(0)
    tester.circuit.I = 1
    tester.advance_cycle()
    tester.circuit.O.expect(1)
    tester.circuit.I = 2
    tester.advance_cycle()
    tester.circuit.O.expect(2)
    tester.circuit.RESET = 1
    tester.advance_cycle()
    tester.circuit.RESET = 0
    tester.circuit.I = 3
    tester.circuit.O.expect(0xDE)
    tester.advance_cycle()
    tester.circuit.O.expect(3)
    tester.compile_and_run("verilator", skip_compile=True,
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"))


def test_reg_of_product():
    class T(m.Product):
        x = m.Bits[8]
        y = m.Bits[4]
        
    class test_reg_of_product(m.Circuit):
        io = m.IO(I=m.In(T), O=m.Out(T)) + m.ClockIO(has_reset=True)
        io.O @= Register(T, T(m.Bits[8](0xDE), m.Bits[4](0xA)),
                         reset_type=m.Reset)()(io.I)

    m.compile("build/test_reg_of_product", test_reg_of_product)

    assert check_files_equal(__file__, f"build/test_reg_of_product.v",
                             f"gold/test_reg_of_product.v")

    tester = fault.SynchronousTester(test_reg_of_product, test_reg_of_product.CLK)
    tester.circuit.I = (0, 1)
    tester.circuit.RESET = 1
    tester.advance_cycle()
    tester.circuit.RESET = 0
    # Reset val
    tester.circuit.O.expect((0xDE, 0xA))
    tester.advance_cycle()
    tester.circuit.O.expect((0, 1))
    tester.circuit.I = (2, 3)
    tester.advance_cycle()
    tester.circuit.O.expect((2, 3))
    tester.circuit.I = (4, 5)
    tester.advance_cycle()
    tester.circuit.O.expect((4, 5))
    tester.circuit.RESET = 1
    tester.advance_cycle()
    tester.circuit.RESET = 0
    tester.circuit.I = (6, 7)
    tester.circuit.O.expect((0xDE, 0xA))
    tester.advance_cycle()
    tester.circuit.O.expect((6, 7))
    tester.compile_and_run("verilator", skip_compile=True,
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"))


def test_reg_of_nested_array():
    T = m.Array[3, m.Bits[8]]
        
    class test_reg_of_nested_array(m.Circuit):
        io = m.IO(I=m.In(T), O=m.Out(T)) + m.ClockIO(has_reset=True)
        io.O @= Register(T, T(m.Bits[8](0xDE), m.Bits[8](0xAD),
                              m.Bits[8](0xBE)), reset_type=m.Reset)()(io.I)

    m.compile("build/test_reg_of_nested_array", test_reg_of_nested_array)

    assert check_files_equal(__file__, f"build/test_reg_of_nested_array.v",
                             f"gold/test_reg_of_nested_array.v")

    tester = fault.SynchronousTester(test_reg_of_nested_array,
                                     test_reg_of_nested_array.CLK)
    tester.circuit.I = [0, 1, 2]
    tester.circuit.RESET = 1
    tester.advance_cycle()
    tester.circuit.RESET = 0
    # Reset val
    tester.circuit.O.expect([0xDE, 0xAD, 0xBE])
    tester.advance_cycle()
    tester.circuit.O.expect([0, 1, 2])
    tester.circuit.I = [2, 3, 4]
    tester.advance_cycle()
    tester.circuit.O.expect([2, 3, 4])
    tester.circuit.I = [5, 6, 7]
    tester.advance_cycle()
    tester.circuit.O.expect([5, 6 ,7])
    tester.circuit.RESET = 1
    tester.advance_cycle()
    tester.circuit.RESET = 0
    tester.circuit.I = [8, 9, 10]
    tester.circuit.O.expect([0xDE, 0xAD, 0xBE])
    tester.advance_cycle()
    tester.circuit.O.expect([8, 9, 10])
    tester.compile_and_run("verilator", skip_compile=True,
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"))


def test_reg_async_resetn():
    T = m.Bits[8]
        
    class test_reg_async_resetn(m.Circuit):
        io = m.IO(I=m.In(T), O=m.Out(T)) + m.ClockIO(has_async_resetn=True)
        io.O @= Register(T, T(0xDE), reset_type=m.AsyncResetN)()(io.I)

    m.compile("build/test_reg_async_resetn", test_reg_async_resetn)

    assert check_files_equal(__file__, f"build/test_reg_async_resetn.v",
                             f"gold/test_reg_async_resetn.v")

    tester = fault.Tester(test_reg_async_resetn, test_reg_async_resetn.CLK)
    tester.circuit.I = 0
    tester.circuit.ASYNCRESETN = 1
    tester.eval()
    tester.circuit.ASYNCRESETN = 0
    tester.eval()
    tester.circuit.ASYNCRESETN = 1
    # Reset val
    tester.circuit.O.expect(0xDE)
    tester.step(2)
    tester.circuit.O.expect(0)
    tester.circuit.I = 1
    tester.step(2)
    tester.circuit.O.expect(1)
    tester.circuit.I = 2
    tester.step(2)
    tester.circuit.O.expect(2)
    tester.circuit.ASYNCRESETN = 0
    tester.eval()
    tester.circuit.ASYNCRESETN = 1
    tester.eval()
    tester.circuit.I = 3
    tester.circuit.O.expect(0xDE)
    tester.step(2)
    tester.circuit.O.expect(3)
    tester.compile_and_run("verilator", skip_compile=True,
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"))


def test_reg_of_product_zero_init():
    class T(m.Product):
        x = m.Bits[8]
        y = m.Bits[4]

    class test_reg_of_product_zero_init(m.Circuit):
        io = m.IO(I=m.In(T), O=m.Out(T)) + m.ClockIO(has_reset=True)
        io.O @= Register(T, reset_type=m.Reset)()(io.I)

    m.compile("build/test_reg_of_product_zero_init",
              test_reg_of_product_zero_init)

    assert check_files_equal(__file__, f"build/test_reg_of_product_zero_init.v",
                             f"gold/test_reg_of_product_zero_init.v")

    tester = fault.SynchronousTester(test_reg_of_product_zero_init,
                                     test_reg_of_product_zero_init.CLK)
    tester.circuit.RESET = 1
    tester.advance_cycle()
    tester.circuit.RESET = 0
    # Reset val
    tester.circuit.O.expect((0xDE, 0xA))


def test_enable_reg():
    class test_enable_reg(m.Circuit):
        io = m.IO(I=m.In(m.Bits[8]), O=m.Out(m.Bits[8]))
        io += m.ClockIO(has_reset=True, has_enable=True)
        io.O @= Register(m.Bits[8], m.Bits[8](0xDE), reset_type=m.Reset,
                         has_enable=True)()(io.I, CE=io.CE)

    m.compile("build/test_enable_reg", test_enable_reg)

    assert check_files_equal(__file__, f"build/test_enable_reg.v",
                             f"gold/test_enable_reg.v")

    tester = fault.SynchronousTester(test_enable_reg, test_enable_reg.CLK)
    tester.circuit.CE = 1
    tester.circuit.I = 0
    tester.circuit.RESET = 1
    tester.advance_cycle()
    tester.circuit.RESET = 0
    # Reset val
    tester.circuit.O.expect(0xDE)
    tester.advance_cycle()
    tester.circuit.O.expect(0)
    tester.circuit.I = 1
    tester.advance_cycle()
    tester.circuit.O.expect(1)
    tester.circuit.CE = 0
    tester.circuit.I = 2
    tester.advance_cycle()
    tester.circuit.O.expect(1)
    # reset priority
    tester.circuit.RESET = 1
    tester.advance_cycle()
    tester.circuit.RESET = 0
    tester.circuit.I = 3
    tester.circuit.O.expect(0xDE)
    tester.advance_cycle()
    tester.circuit.O.expect(0xDE)
    tester.compile_and_run("verilator", skip_compile=True,
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"))
