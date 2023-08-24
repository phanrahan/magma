import magma as m
from magma.testing import check_files_equal
import logging
import pytest
import coreir


class And2(m.Circuit):
    name = "And2"
    io = m.IO(I0=m.In(m.Bit), I1=m.In(m.Bit), O=m.Out(m.Bit))


@pytest.mark.parametrize("target,suffix",
                         [("verilog", "v"), ("coreir", "json")])
def test_simple_def(target, suffix):
    m.config.set_debug_mode(True)
    m.set_codegen_debug_info(True)

    class main(m.Circuit):
        name = "main"
        io = m.IO(I=m.In(m.Bits[2]), O=m.Out(m.Bit))
        and2 = And2()

        m.wire(io.I[0], and2.I0)
        m.wire(io.I[1], and2.I1)
        m.wire(and2.O, io.O)


    m.compile("build/test_simple_def", main, output=target)
    assert check_files_equal(__file__, f"build/test_simple_def.{suffix}",
                             f"gold/test_simple_def.{suffix}")

    # Check that the subclassing pattern produces the same annotations
    class Main(m.Circuit):
        io = m.IO(I=m.In(m.Bits[2]), O=m.Out(m.Bit))

        and2 = And2()
        m.wire(io.I[0], and2.I0)
        m.wire(io.I[1], and2.I1)
        m.wire(and2.O, io.O)

    # Create a fresh context for second compilation.
    m.compile("build/test_simple_def_class", Main, output=target)
    m.set_codegen_debug_info(False)
    m.config.set_debug_mode(False)
    assert check_files_equal(__file__, f"build/test_simple_def_class.{suffix}",
                             f"gold/test_simple_def_class.{suffix}")


@pytest.mark.parametrize("target,suffix",
                         [("verilog", "v"), ("coreir", "json")])
def test_for_loop_def(target, suffix):
    m.config.set_debug_mode(True)
    m.set_codegen_debug_info(True)

    class main(m.Circuit):
        name = "main"
        io = m.IO(I=m.In(m.Bits[2]), O=m.Out(m.Bit))
        and2_prev = None
        for i in range(0, 4):
            and2 = And2()
            if i == 0:
                m.wire(io.I[0], and2.I0)
                m.wire(io.I[1], and2.I1)
            else:
                m.wire(and2_prev.O, and2.I0)
                m.wire(io.I[1], and2.I1)
            and2_prev = and2

        m.wire(and2.O, io.O)


    m.compile("build/test_for_loop_def", main, output=target)
    m.set_codegen_debug_info(False)
    m.config.set_debug_mode(False)
    assert check_files_equal(__file__, f"build/test_for_loop_def.{suffix}",
                             f"gold/test_for_loop_def.{suffix}")


@pytest.mark.parametrize("target,suffix",
                         [("verilog", "v"), ("coreir", "json")])
def test_interleaved_instance_wiring(target, suffix):
    m.config.set_debug_mode(True)
    m.set_codegen_debug_info(True)

    class main(m.Circuit):
        name = "main"
        io = m.IO(I=m.In(m.Bits[2]), O=m.Out(m.Bit))
        and2_0 = And2()
        and2_1 = And2()

        m.wire(io.I[0], and2_0.I0)
        m.wire(io.I[1], and2_0.I1)
        m.wire(and2_0.O, and2_1.I0)
        m.wire(io.I[1], and2_1.I1)
        and2_2 = And2()
        m.wire(and2_1.O, and2_2.I0)
        m.wire(io.I[0], and2_2.I1)

        m.wire(and2_2.O, io.O)


    m.compile("build/test_interleaved_instance_wiring", main, output=target)
    m.set_codegen_debug_info(False)
    m.config.set_debug_mode(False)
    assert check_files_equal(__file__, f"build/test_interleaved_instance_wiring.{suffix}",
                             f"gold/test_interleaved_instance_wiring.{suffix}")


def test_unwired_ports_warnings(caplog):
    caplog.set_level(logging.WARN)

    class main(m.Circuit):
        name = "main"
        io = m.IO(I=m.In(m.Bits[2]), O=m.Out(m.Bit))
        and2 = And2()

        m.wire(io.I[1], and2.I1)


    m.compile("build/test_unwired_output", main, "verilog")
    assert check_files_equal(__file__, f"build/test_unwired_output.v",
                             f"gold/test_unwired_output.v")
    assert caplog.records[-2].msg == "main.And2_inst0.I0 not connected"
    assert caplog.records[-1].msg == "main.O is unwired"


def test_2d_array_error(caplog):

    class main(m.Circuit):
        name = "main"
        io = m.IO(I=m.In(m.Array[2, m.Array[3, m.Bit]]),
                           O=m.Out(m.Bit))
        and2 = And2()

        m.wire(io.I[1][0], and2.I1)


    try:
        m.compile("build/test_unwired_output", main, output="verilog")
        assert False, "Should raise exception"
    except Exception as e:
        print(str(e))
        assert str(e) == "Argument main.I of type Array[(2, Array[(3, Out(Bit))])] is not supported, the verilog backend only supports simple 1-d array of bits of the form Array(N, Bit)"  # noqa


class XY(m.Product):
    x = m.Bit
    y = m.Bit


@pytest.mark.parametrize("target,suffix",
                         [("verilog", "v"), ("coreir", "json")])
@pytest.mark.parametrize("T", [m.Bit, m.Bits[2], m.Array[2, m.Bit], XY])
def test_anon_value(target, suffix, T):

    class And2(m.Circuit):
        name = "And2"
        io = m.IO(I0=m.In(T), I1=m.In(T), O=m.Out(T))

    class main(m.Circuit):
        name = "main"
        io = m.IO(I0=m.In(T), I1=m.In(T),
                           O=m.Out(T))
        and2 = And2()

        m.wire(io.I0, and2.I0)
        m.wire(io.I1, and2.I1)
        tmp = T()
        m.wire(and2.O, tmp)
        m.wire(tmp, io.O)


    type_str = str(T).replace("[", "(").replace("]", ")")
    m.compile(f"build/test_anon_value_{type_str}", main, target)
    assert check_files_equal(__file__, f"build/test_anon_value_{type_str}.{suffix}",
                             f"gold/test_anon_value_{type_str}.{suffix}")


if __name__ == "__main__":
    test_simple_def("coreir", "json")
