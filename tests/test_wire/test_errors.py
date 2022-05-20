import magma as m

from magma import *
from magma.common import wrap_with_context_manager
from magma.logging import logging_level
from magma.testing.utils import (
    has_error, has_warning, magma_debug_section
)


def test_input_as_output(caplog):
    magma.config.set_debug_mode(True)
    class Buf(Circuit):
        name = "Buf"
        io = IO(I=In(Bit), O=Out(Bit))

    class main(Circuit):
        name = "main"
        io = IO(I=In(Bit), O=Out(Bit))
        buf = Buf()
        wire(io.O, buf.I)
    msg = """\
\033[1mtests/test_wire/test_errors.py:21\033[0m: Cannot wire main.O (In(Bit)) to main.buf.I (In(Bit))
>>         wire(io.O, buf.I)"""
    assert has_error(caplog, msg)
    magma.config.set_debug_mode(False)


def test_output_as_input(caplog):
    magma.config.set_debug_mode(True)
    class A(Circuit):
        name = "A"
        io = IO(I=In(Bit), O=Out(Bit))

    class main(Circuit):
        name = "main"
        io = IO(I=In(Bit), O=Out(Bit))
        a = A()
        wire(io.I, a.O)
    msg = """\
\033[1mtests/test_wire/test_errors.py:39\033[0m: Cannot wire main.I (Out(Bit)) to main.a.O (Out(Bit))
>>         wire(io.I, a.O)"""
    assert has_error(caplog, msg)
    magma.config.set_debug_mode(False)


def test_multiple_outputs_to_input_warning(caplog):
    magma.config.set_debug_mode(True)
    class A(Circuit):
        name = "A"
        io = IO(I=In(Bit), O=Out(Bit))

    class main(Circuit):
        name = "main"
        io = IO(I=In(Bits[2]), O=Out(Bit))
        a = A()
        wire(io.I[0], a.I)
        wire(io.I[1], a.I)
    msg = """\
\033[1mtests/test_wire/test_errors.py:58\033[0m: Wiring multiple outputs to same wire, using last connection. Input: main.a.I, Old Output: main.I[0], New Output: main.I[1]
>>         wire(io.I[1], a.I)"""
    assert has_warning(caplog, msg)
    magma.config.set_debug_mode(False)


def test_multiple_outputs_circuit(caplog):
    magma.config.set_debug_mode(True)
    class A(Circuit):
        name = "A"
        io = IO(I=In(Bit), O=Out(Bit), U=Out(Bit))

    class main(Circuit):
        name = "main"
        io = IO(I=In(Bits[2]), O=Out(Bit))
        a = A()
        wire(a, io.I)
    msg = """\
\033[1mtests/test_wire/test_errors.py:76\033[0m: Can only wire circuits with one output; circuit `main.a` has outputs ['O', 'U']
>>         wire(a, io.I)"""
    assert has_error(caplog, msg)
    magma.config.set_debug_mode(False)


def test_mismatch_outputs_circuit(caplog):
    magma.config.set_debug_mode(True)
    class A(Circuit):
        name = "A"
        io = IO(I=In(Bit), J=In(Bit), O=Out(Bit), U=Out(Bit))

    class Main(Circuit):
        name = "main"
        io = IO(I=In(Bit), O=Out(Bit))

    class Foo(Circuit):
        a = A()
        main = Main()
        a(main)
    msg = """\
\033[1mtests/test_wire/test_errors.py:97\033[0m: Number of inputs is not equal to the number of outputs, expected 2 inputs, got 1. Only 1 will be wired.
>>         a(main)"""
    assert has_warning(caplog, msg)
    magma.config.set_debug_mode(False)


def test_no_inputs_circuit(caplog):
    magma.config.set_debug_mode(True)
    class A(Circuit):
        name = "A"
        io = IO(O=Out(Bit), U=Out(Bit))

    class main(Circuit):
        name = "main"
        io = IO(I=In(Bit), O=Out(Bit))
        a = A()
        wire(io.I, a)
    msg = """\
\033[1mtests/test_wire/test_errors.py:115\033[0m: Wiring an output to a circuit with no input arguments, skipping
>>         wire(io.I, a)"""
    assert has_warning(caplog, msg)
    magma.config.set_debug_mode(False)


def test_multiple_inputs_circuit(caplog):
    magma.config.set_debug_mode(True)
    class A(Circuit):
        name = "A"
        io = IO(I=In(Bit), J=In(Bit), O=Out(Bit), U=Out(Bit))

    class main(Circuit):
        name = "main"
        io = IO(I=In(Bit), O=Out(Bit))
        a = A()
        wire(io.I, a)
    msg = """\
\033[1mtests/test_wire/test_errors.py:133\033[0m: Wiring an output to a circuit with more than one input argument, using the first input main.a.I
>>         wire(io.I, a)"""
    assert has_warning(caplog, msg)
    magma.config.set_debug_mode(False)


def test_no_key(caplog):
    magma.config.set_debug_mode(True)
    class A(Circuit):
        name = "A"
        io = IO(I=In(Bit), J=In(Bit), O=Out(Bit), U=Out(Bit))

    class main(Circuit):
        name = "main"
        io = IO(I=In(Bit), O=Out(Bit))
        a = A()
        a(K=io.I)
    msg = """\
\033[1mtests/test_wire/test_errors.py:151\033[0m: Instance main.a does not have input K
>>         a(K=io.I)"""

    assert has_warning(caplog, msg)
    magma.config.set_debug_mode(False)


def test_const_array_error(caplog):
    magma.config.set_debug_mode(True)
    class Buf(Circuit):
        name = "Buf"
        io = IO(I=In(Array[1, Bit]), O=Out(Array[1, Bit]))

    class main(Circuit):
        name = "main"
        io = IO(O=Out(Array[1, Bit]))
        buf = Buf()

        wire(1, buf.I)
        wire(buf.O, io.O)

    msg = """\
\033[1mtests/test_wire/test_errors.py:171\033[0m: Cannot wire 1 (<class 'int'>) to main.buf.I (Array[(1, In(Bit))])
>>         wire(1, buf.I)"""
    assert caplog.records[0].msg == msg
    assert has_error(caplog, msg)
    magma.config.set_debug_mode(False)


@wrap_with_context_manager(logging_level("DEBUG"))
def test_hanging_anon_error(caplog):
    with magma_debug_section():
        class _Foo(m.Circuit):
            T = m.Bits[8]
            io = m.IO(I=m.In(T), O=m.Out(T))
            io.O @= m.Bits[8]()

        try:
            m.compile("Foo", _Foo, output="coreir")
            assert False, "Did not raise excpected exception"
        except Exception as e:
            assert str(e) == "Found circuit with errors: _Foo"

        msg = """\
\033[1mtests/test_wire/test_errors.py:185\033[0m: _Foo.O not driven
>>         class _Foo(m.Circuit):"""
        assert caplog.records[0].message == msg
        assert has_error(caplog, msg)
        msg = "_Foo.O: Unconnected"
        assert caplog.records[1].message == msg
        assert has_error(caplog, msg)


def test_wire_tuple_to_clock():
    class T(m.Product):
        a = m.In(m.Clock)
        b = m.In(m.Clock)

    class Foo(m.Circuit):
        io = m.IO(I=In(T), O=m.Out(m.Clock), x=m.Out(m.Bit))
        m.wire(io.I, io.O)
        # Wire a dummy output so we don't have an empty defn
        io.x @= 1

    # Imported here to avoid changing line numbers for above tests
    import pytest
    with pytest.raises(Exception) as e:
        m.compile("build/Foo", Foo)
    assert str(e.value) == "Found circuit with errors: Foo"
