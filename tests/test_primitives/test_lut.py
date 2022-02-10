import os

import magma as m
from magma.testing import check_files_equal
from magma.primitives import LUT

import fault


def test_basic_lut():
    class test_basic_lut(m.Circuit):
        contents = (
            m.Bits[8](0xDE),
            m.Bits[8](0xAD),
            m.Bits[8](0xBE),
            m.Bits[8](0xEF)
        )
        io = m.IO(I=m.In(m.Bits[2]), O=m.Out(m.Bits[8]))
        io.O @= LUT(m.Bits[8], contents)()(io.I)

    m.compile("build/test_basic_lut", test_basic_lut)

    assert check_files_equal(__file__, f"build/test_basic_lut.v",
                             f"gold/test_basic_lut.v")

    tester = fault.Tester(test_basic_lut)
    for i in range(0, 4):
        tester.circuit.I = i
        tester.eval()
        tester.circuit.O.expect(int(test_basic_lut.contents[i]))
    tester.compile_and_run("verilator", skip_compile=True,
                           flags=["-Wno-unused"],
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"))


def test_lut_bit():
    contents = (
        m.Bit(True),
        m.Bit(False),
        m.Bit(True),
        m.Bit(False)
    )

    class test_lut_bit(m.Circuit):
        io = m.IO(I=m.In(m.Bits[2]), O=m.Out(m.Bit))
        io.O @= LUT(m.Bit, contents)()(io.I)

    m.compile("build/test_lut_bit", test_lut_bit)

    assert check_files_equal(__file__, f"build/test_lut_bit.v",
                             f"gold/test_lut_bit.v")

    tester = fault.Tester(test_lut_bit)
    for i in range(0, 4):
        tester.circuit.I = i
        tester.eval()
        tester.circuit.O.expect(True if contents[i] is m.Bit.VCC else False)
    tester.compile_and_run("verilator", skip_compile=True,
                           flags=["-Wno-unused"],
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"))


def test_lut_nested_array():
    class test_lut_nested_array(m.Circuit):
        contents = (
            m.Array[2, m.Bits[2]]([m.Bits[2](3), m.Bits[2](0x1)]),
            m.Array[2, m.Bits[2]]([m.Bits[2](0), m.Bits[2](0x2)])
        )
        io = m.IO(I=m.In(m.Bits[1]), O=m.Out(m.Array[2, m.Bits[2]]))
        io.O @= LUT(m.Array[2, m.Bits[2]], contents)()(io.I)

    m.compile("build/test_lut_nested_array", test_lut_nested_array)

    assert check_files_equal(__file__, f"build/test_lut_nested_array.v",
                             f"gold/test_lut_nested_array.v")

    tester = fault.Tester(test_lut_nested_array)
    for i in range(0, 2):
        tester.circuit.I = i
        tester.eval()
        for j in range(2):
            tester.circuit.O[j].expect(int(test_lut_nested_array.contents[i][j]))
    tester.compile_and_run("verilator", skip_compile=True,
                           flags=["-Wno-unused"],
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"))


def test_lut_tuple():
    class test_lut_tuple(m.Circuit):
        contents = (
            m.Tuple[m.Bit, m.Bits[2]](m.Bit(True), m.Bits[2](2)),
            m.Tuple[m.Bit, m.Bits[2]](m.Bit(False), m.Bits[2](3))
        )

        io = m.IO(I=m.In(m.Bits[1]), O=m.Out(m.Tuple[m.Bit, m.Bits[2]]))
        io.O @= LUT(m.Tuple[m.Bit, m.Bits[2]], contents)()(io.I)

    m.compile("build/test_lut_tuple", test_lut_tuple)

    assert check_files_equal(__file__, f"build/test_lut_tuple.v",
                             f"gold/test_lut_tuple.v")

    tester = fault.Tester(test_lut_tuple)
    for i in range(0, 2):
        tester.circuit.I = i
        tester.eval()
        for j in range(2):
            value = test_lut_tuple.contents[i][j]
            if isinstance(value, m.Bit):
                value = True if value is m.Bit.VCC else False
            else:
                value = int(value)
            tester.circuit.O[j].expect(value)
    tester.compile_and_run("verilator", skip_compile=True,
                           flags=["-Wno-unused"],
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"))


def test_lut_arr_of_product():
    class A(m.Product):
        X = m.Bit
        Y = m.Bits[2]

    class test_lut_arr_of_product(m.Circuit):
        contents = (
            m.Array[2, A]([A(m.Bit(True), m.Bits[2](0)),
                           A(m.Bit(False), m.Bits[2](1))]),
            m.Array[2, A]([A(m.Bit(False), m.Bits[2](2)),
                           A(m.Bit(True), m.Bits[2](3))])
        )

        io = m.IO(I=m.In(m.Bits[1]), O=m.Out(m.Array[2, A]))
        io.O @= LUT(m.Array[2, A], contents)()(io.I)

    m.compile("build/test_lut_arr_of_product", test_lut_arr_of_product)

    assert check_files_equal(__file__, f"build/test_lut_arr_of_product.v",
                             f"gold/test_lut_arr_of_product.v")

    tester = fault.Tester(test_lut_arr_of_product)
    for i in range(0, 2):
        tester.circuit.I = i
        tester.eval()
        for j in range(2):
            for attr in ["X", "Y"]:
                value = getattr(test_lut_arr_of_product.contents[i][j], attr)
                if isinstance(value, m.Bit):
                    value = True if value is m.Bit.VCC else False
                else:
                    value = int(value)
                getattr(tester.circuit.O[j], attr).expect(value)
    tester.compile_and_run("verilator", skip_compile=True,
                           flags=["-Wno-unused"],
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"))
