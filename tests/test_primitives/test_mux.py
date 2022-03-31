import os
import pytest

import fault
import hwtypes as ht
import magma as m
from magma.testing import check_files_equal, SimpleMagmaProtocol


def test_basic_mux():
    class test_basic_mux(m.Circuit):
        io = m.IO(I=m.In(m.Bits[2]), S=m.In(m.Bit), O=m.Out(m.Bit))
        io.O @= m.Mux(2, m.Bit)()(io.I[0], io.I[1], io.S)

    m.compile("build/test_basic_mux", test_basic_mux)

    assert check_files_equal(__file__, f"build/test_basic_mux.v",
                             f"gold/test_basic_mux.v")

    tester = fault.Tester(test_basic_mux)
    tester.circuit.I = 1
    tester.circuit.S = 0
    tester.eval()
    tester.circuit.O.expect(1)
    tester.circuit.S = 1
    tester.eval()
    tester.circuit.O.expect(0)
    tester.compile_and_run("verilator", skip_compile=True,
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"))


def test_basic_mux_bits():
    class test_basic_mux_bits(m.Circuit):
        io = m.IO(I=m.In(m.Array[2, m.Bits[2]]), S=m.In(m.Bit), O=m.Out(m.Bits[2]))
        io.O @= m.Mux(2, m.Bits[2])()(io.I[0], io.I[1], io.S)

    m.compile("build/test_basic_mux_bits", test_basic_mux_bits)

    assert check_files_equal(__file__, f"build/test_basic_mux_bits.v",
                             f"gold/test_basic_mux_bits.v")

    tester = fault.Tester(test_basic_mux_bits)
    tester.circuit.I = [1, 2]
    tester.circuit.S = 0
    tester.eval()
    tester.circuit.O.expect(1)
    tester.circuit.S = 1
    tester.eval()
    tester.circuit.O.expect(2)
    tester.compile_and_run("verilator", skip_compile=True,
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"))


def test_basic_mux_arr():
    T = m.Array[2, m.Bits[2]]

    class test_basic_mux_arr(m.Circuit):
        io = m.IO(I=m.In(m.Array[2, T]), S=m.In(m.Bit), O=m.Out(T))
        io.O @= m.Mux(2, T)()(io.I[0], io.I[1], io.S)

    m.compile("build/test_basic_mux_arr", test_basic_mux_arr, inline=True)

    assert check_files_equal(__file__, f"build/test_basic_mux_arr.v",
                             f"gold/test_basic_mux_arr.v")

    tester = fault.Tester(test_basic_mux_arr)
    tester.circuit.I = [[0, 1], [2, 3]]
    tester.circuit.S = 0
    tester.eval()
    tester.circuit.O.expect([0, 1])
    tester.circuit.S = 1
    tester.eval()
    tester.circuit.O.expect([2, 3])
    tester.compile_and_run("verilator", skip_compile=True,
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"))


def test_basic_mux_tuple():
    T = m.Tuple[m.Bit, m.Bits[2]]

    class test_basic_mux_tuple(m.Circuit):
        io = m.IO(I=m.In(m.Array[2, T]), S=m.In(m.Bit), O=m.Out(T))
        io.O @= m.Mux(2, T)()(io.I[0], io.I[1], io.S)

    m.compile("build/test_basic_mux_tuple", test_basic_mux_tuple, inline=True)

    assert check_files_equal(__file__, f"build/test_basic_mux_tuple.v",
                             f"gold/test_basic_mux_tuple.v")

    tester = fault.Tester(test_basic_mux_tuple)
    tester.circuit.I = [(True, 1), (False, 3)]
    tester.circuit.S = 0
    tester.eval()
    tester.circuit.O.expect((True, 1))
    tester.circuit.S = 1
    tester.eval()
    tester.circuit.O.expect((False, 3))
    tester.compile_and_run("verilator", skip_compile=True,
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"))


def test_basic_mux_product():
    class T(m.Product):
        X = m.Bits[2]
        Y = m.Bits[4]

    class test_basic_mux_product(m.Circuit):
        io = m.IO(I=m.In(m.Array[2, T]), S=m.In(m.Bit), O=m.Out(T))
        io.O @= m.Mux(2, T)()(io.I[0], io.I[1], io.S)

    m.compile("build/test_basic_mux_product", test_basic_mux_product,
              inline=True)

    assert check_files_equal(__file__, f"build/test_basic_mux_product.v",
                             f"gold/test_basic_mux_product.v")

    tester = fault.Tester(test_basic_mux_product)
    tester.circuit.I = [{"X": 2, "Y": 5}, {"X": 0, "Y": 7}]
    tester.circuit.S = 0
    tester.eval()
    tester.circuit.O.expect({"X": 2, "Y": 5})
    tester.circuit.S = 1
    tester.eval()
    tester.circuit.O.expect({"X": 0, "Y": 7})
    tester.compile_and_run("verilator", skip_compile=True,
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"))


def test_mux_operator():
    class test_mux_operator(m.Circuit):
        io = m.IO(I=m.In(m.Bits[2]), S=m.In(m.Bit), O=m.Out(m.Bit))
        io.O @= m.mux([io.I[0], io.I[1]], io.S, name="foo")

    m.compile("build/test_mux_operator", test_mux_operator)

    assert check_files_equal(__file__, f"build/test_mux_operator.v",
                             f"gold/test_mux_operator.v")

    tester = fault.Tester(test_mux_operator)
    tester.circuit.I = 1
    tester.circuit.S = 0
    tester.eval()
    tester.circuit.O.expect(1)
    tester.circuit.S = 1
    tester.eval()
    tester.circuit.O.expect(0)
    tester.compile_and_run("verilator", skip_compile=True,
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"))


def test_mux_operator_int():
    class test_mux_operator_int(m.Circuit):
        io = m.IO(I=m.In(m.Bit), S=m.In(m.Bit), O=m.Out(m.Bit))
        io.O @= m.mux([0, io.I], io.S)

    m.compile("build/test_mux_operator_int", test_mux_operator_int)

    assert check_files_equal(__file__, f"build/test_mux_operator_int.v",
                             f"gold/test_mux_operator_int.v")

    tester = fault.Tester(test_mux_operator_int)
    tester.circuit.I = 1
    tester.circuit.S = 0
    tester.eval()
    tester.circuit.O.expect(0)
    tester.circuit.S = 1
    tester.eval()
    tester.circuit.O.expect(1)
    tester.compile_and_run("verilator", skip_compile=True,
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"))


def test_mux_operator_tuple():
    class test_mux_operator_tuple(m.Circuit):
        io = m.IO(S=m.In(m.Bit), O0=m.Out(m.Bit), O1=m.Out(m.Bits[2]),
                  O2=m.Out(m.Bit))
        O0, O1, O2 = m.mux([
            (True, ht.BitVector[2](3), ht.Bit(0)),
            (False, ht.BitVector[2](0), ht.Bit(1))
        ], io.S)
        io.O0 @= O0
        io.O1 @= O1
        io.O2 @= O2

    m.compile("build/test_mux_operator_tuple", test_mux_operator_tuple)

    tester = fault.Tester(test_mux_operator_tuple)
    tester.circuit.S = 0
    tester.eval()
    tester.circuit.O0.expect(1)
    tester.circuit.O1.expect(3)
    tester.circuit.O2.expect(0)
    tester.circuit.S = 1
    tester.eval()
    tester.circuit.O0.expect(0)
    tester.circuit.O1.expect(0)
    tester.circuit.O2.expect(1)
    tester.compile_and_run("verilator", skip_compile=True,
                           flags=["-Wno-unused"],
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"))


def test_mux_tuple_wire():
    default = (ht.BitVector.random(3), ht.BitVector.random(5))
    inst_map = {
        0: (ht.BitVector.random(3), ht.BitVector.random(5)),
        1: (ht.BitVector.random(3), ht.BitVector.random(5)),
    }

    class Main(m.Circuit):
        io = m.IO(inst=m.In(m.Bit))
        ctrl_signals = default
        for inst, signals in reversed(tuple(inst_map.items())):
            ctrl_signals = m.mux([ctrl_signals, signals], io.inst == inst)


def test_mux_dict_lookup():
    class test_mux_dict_lookup(m.Circuit):
        io = m.IO(S=m.In(m.Bits[2]), O=m.Out(m.Bits[5]))

        dict_ = {
            0: ht.BitVector[5](0),
            2: ht.BitVector[5](2),
            3: ht.BitVector[5](3)
        }
        io.O @= m.dict_lookup(dict_, io.S, ht.BitVector[5](1))

    m.compile("build/test_mux_dict_lookup", test_mux_dict_lookup)

    tester = fault.Tester(test_mux_dict_lookup)
    for i in range(4):
        tester.circuit.S = i
        tester.eval()
        tester.circuit.O.expect(i)

    tester.compile_and_run("verilator", skip_compile=True,
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"),
                           flags=["-Wno-unused"])


def test_mux_list_lookup():
    class test_mux_list_lookup(m.Circuit):
        io = m.IO(S=m.In(m.Bits[2]), O=m.Out(m.Bits[5]))

        list_ = [ht.BitVector[5](0), ht.BitVector[5](1), ht.BitVector[5](2)]
        io.O @= m.list_lookup(list_, io.S, ht.BitVector[5](3))

    m.compile("build/test_mux_list_lookup", test_mux_list_lookup)

    tester = fault.Tester(test_mux_list_lookup)
    for i in range(4):
        tester.circuit.S = i
        tester.eval()
        tester.circuit.O.expect(i)

    tester.compile_and_run("verilator", skip_compile=True,
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"),
                           flags=["-Wno-unused"])


def test_mux_array_select_bits_1():
    depth = 2
    N = 8
    class test_mux_array_select_bits_1(m.Circuit):
        io = m.IO(
            I=m.In(m.Array[depth, m.Bits[N]]),
            O=m.Out(m.Bits[N])
        ) + m.ClockIO()
        ptr_width = m.bitutils.clog2(depth)
        ptr = m.Register(m.Bits[ptr_width])()
        io.O @= io.I[ptr.O]
        ptr.I @= ptr.O + 1

    m.compile("build/test_mux_array_select_bits_1",
              test_mux_array_select_bits_1)

    tester = fault.SynchronousTester(test_mux_array_select_bits_1,
                                     test_mux_array_select_bits_1.CLK)
    tester.circuit.I = I = [0xDE, 0xAD]
    tester.advance_cycle()
    tester.circuit.O.expect(I[1])
    tester.advance_cycle()
    tester.circuit.O.expect(I[0])

    tester.compile_and_run("verilator", skip_compile=True,
                           flags=["-Wno-unused"],
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"))


@pytest.mark.parametrize("ht_T, m_T", [(ht.UIntVector, m.UInt),
                                       (ht.SIntVector, m.SInt)])
def test_mux_intv(ht_T, m_T):
    class Main(m.Circuit):
        O = m.mux([ht_T[4](1), m_T[4](2)], m.Bit())
        assert isinstance(O, m_T)


@pytest.mark.parametrize("ht_T", [ht.UIntVector, ht.SIntVector])
def test_mux_intv_bits(ht_T):
    class Main(m.Circuit):
        O = m.mux([ht_T[4](1), m.Bits[4](2)], m.Bit())
        assert type(O) is m.Out(m.Bits[4])


def test_mux_signed_unsigned():
    class Main(m.Circuit):
        io = m.IO(a=m.In(m.SInt[16]), b=m.In(m.UInt[16]), s=m.In(m.Bit))

        with pytest.raises(TypeError) as e:
            m.mux([io.a, io.b], io.s)

        assert str(e.value) == (
            "Found incompatible types UInt[16] and SInt[16] in mux inference"
        )


def test_mux_protocol():
    T = SimpleMagmaProtocol[m.Bits[8]]

    class _(m.Circuit):
        x, y = T(), T()
        s = m.Bit()
        out = m.mux([x, y], s)
        assert isinstance(out, T)

    Mux = m.Mux(2, T)
    assert isinstance(Mux.I0, m.Out(T))
    assert isinstance(Mux.I1, m.Out(T))
    assert isinstance(Mux.O, m.In(T))


@pytest.mark.parametrize("n,use_bit", ((2, True), (2, False), (8, True),))
def test_mux_operator_const_select(n, use_bit):
    T = m.Bits[8]
    sel_bits = m.bitutils.clog2(n)
    T_sel = m.Bit if (sel_bits == 1 and use_bit) else m.Bits[sel_bits]

    class _(m.Circuit):
        vec = [T() for _ in range(n)]
        sel = T_sel(0) if sel_bits == 1 else T_sel(0)
        m.mux(vec, sel)
