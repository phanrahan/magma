import magma as m
from magma.testing import check_files_equal
import logging
import pytest


@pytest.mark.parametrize("target,suffix",
                         [("verilog", "v"), ("coreir", "json")])
def test_simple_def(target, suffix):
    m.set_codegen_debug_info(True)
    And2 = m.DeclareCircuit('And2', "I0", m.In(m.Bit), "I1", m.In(m.Bit),
                            "O", m.Out(m.Bit))

    main = m.DefineCircuit("main", "I", m.In(m.Bits(2)), "O", m.Out(m.Bit))

    and2 = And2()

    m.wire(main.I[0], and2.I0)
    m.wire(main.I[1], and2.I1)
    m.wire(and2.O, main.O)

    m.EndCircuit()

    m.compile("build/test_simple_def", main, output=target)
    assert check_files_equal(__file__, f"build/test_simple_def.{suffix}",
                             f"gold/test_simple_def.{suffix}")

    # Check that the subclassing pattern produces the same annotations
    class Main(m.Circuit):
        IO = ["I", m.In(m.Bits(2)), "O", m.Out(m.Bit)]

        @classmethod
        def definition(io):
            and2 = And2()
            m.wire(io.I[0], and2.I0)
            m.wire(io.I[1], and2.I1)
            m.wire(and2.O, io.O)

    m.compile("build/test_simple_def_class", Main, output=target)
    m.set_codegen_debug_info(False)
    assert check_files_equal(__file__, f"build/test_simple_def_class.{suffix}",
                             f"gold/test_simple_def_class.{suffix}")


def test_unwired_ports_warnings(caplog):
    caplog.set_level(logging.WARN)
    And2 = m.DeclareCircuit('And2', "I0", m.In(m.Bit), "I1", m.In(m.Bit),
                            "O", m.Out(m.Bit))

    main = m.DefineCircuit("main", "I", m.In(m.Bits(2)), "O", m.Out(m.Bit))

    and2 = And2()

    m.wire(main.I[1], and2.I1)

    m.EndCircuit()

    m.compile("build/test_unwired_output", main)
    assert check_files_equal(__file__, f"build/test_unwired_output.v",
                             f"gold/test_unwired_output.v")
    assert caplog.records[0].msg == "main.And2_inst0.I0 not connected"
    assert caplog.records[1].msg == "main.O is unwired"


def test_2d_array_error(caplog):
    And2 = m.DeclareCircuit('And2', "I0", m.In(m.Bit), "I1", m.In(m.Bit),
                            "O", m.Out(m.Bit))

    main = m.DefineCircuit("main", "I", m.In(m.Array(2, m.Array(3, m.Bit))),
                           "O", m.Out(m.Bit))

    and2 = And2()

    m.wire(main.I[1][0], and2.I1)

    m.EndCircuit()

    try:
        m.compile("build/test_unwired_output", main)
        assert False, "Should raise exception"
    except Exception as e:
        assert str(e) == "Argument main.I of type Array(2,Array(3,Out(Bit))) is not supported, the verilog backend only supports simple 1-d array of bits of the form Array(N, Bit)"  # noqa


@pytest.mark.parametrize("target,suffix",
                         [("verilog", "v"), ("coreir", "json")])
def test_anon_bit(target, suffix):
    And2 = m.DeclareCircuit('And2', "I0", m.In(m.Bit), "I1", m.In(m.Bit),
                            "O", m.Out(m.Bit))

    main = m.DefineCircuit("main", "I", m.In(m.Bits(2)),
                           "O", m.Out(m.Bit))

    and2 = And2()

    m.wire(main.I[0], and2.I0)
    m.wire(main.I[1], and2.I1)
    tmp = m.Bit()
    m.wire(and2.O, tmp)
    m.wire(tmp, main.O)

    m.EndCircuit()

    m.compile("build/test_anon_bit", main, target)
    assert check_files_equal(__file__, f"build/test_anon_bit.{suffix}",
                             f"gold/test_anon_bit.{suffix}")
