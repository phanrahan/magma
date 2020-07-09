import magma as m

from magma import *
from magma.testing.utils import has_error, has_warning, magma_debug_section


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
\033[1mtests/test_wire/test_errors.py:15\033[0m: Using `.O` (an input) as an output
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
\033[1mtests/test_wire/test_errors.py:33\033[0m: Using `..O` (an output) as an input
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
\033[1mtests/test_wire/test_errors.py:52\033[0m: Wiring multiple outputs to same wire, using last connection. Input: ..I,  Old Output: LazyCircuit.I[0],  New Output: LazyCircuit.I[1]
>>         wire(io.I[1], a.I)"""
    assert has_warning(caplog, msg)
    magma.config.set_debug_mode(False)


def test_muliple_outputs_circuit(caplog):
    magma.config.set_debug_mode(True)
    class A(Circuit):
        name = "A"
        io = IO(I=In(Bit), O=Out(Bit), U=Out(Bit))

    class main(Circuit):
        name = "main"
        io = IO(I=In(Bits(2)), O=Out(Bit))
        a = A()
        wire(a, io.I)
    msg = """\
\033[1mtests/test_wire/test_errors.py:60\033[0m: Can only wire circuits with one output. Argument 0 to wire `.a` has outputs [inst0.O, inst0.U]
>>         wire(a, .I)"""
    assert has_warning(caplog, msg)
    magma.config.set_debug_mode(False)


def test_muliple_outputs_circuit(caplog):
    magma.config.set_debug_mode(True)
    class A(Circuit):
        name = "A"
        io = IO(I=In(Bit), J=In(Bit), O=Out(Bit), U=Out(Bit))

    class main(Circuit):
        name = "main"
        io = IO(I=In(Bit), O=Out(Bit))
        a = A()
    main.a(main)
    msg = """\
\033[1mtests/test_wire/test_errors.py:88\033[0m: Number of inputs is not equal to the number of outputs, expected 2 inputs, got 1. Only 1 will be wired.
>>     main.a(main)"""
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
\033[1mtests/test_wire/test_errors.py:106\033[0m: Wiring an output to a circuit with no input arguments, skipping
>>         wire(io.I, a)"""
    assert has_warning(caplog, msg)
    magma.config.set_debug_mode(False)


def test_muliple_inputs_circuit(caplog):
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
\033[1mtests/test_wire/test_errors.py:124\033[0m: Wiring an output to a circuit with more than one input argument, using the first input ..I
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
\033[1mtests/test_wire/test_errors.py:142\033[0m: Instance . does not have input K
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
\033[1mtests/test_wire/test_errors.py:162\033[0m: Cannot wire 1 (type=<class 'int'>) to ..I (type=Array[1, In(Bit)]) because conversions from IntegerTypes are only defined for Bits, not general Arrays
>>         wire(1, buf.I)"""
    assert caplog.records[0].msg == msg
    assert has_error(caplog, msg)
    magma.config.set_debug_mode(False)


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
            assert str(e) == "Found unconnected port: _Foo.O"

        msg = """\
\033[1mtests/test_wire/test_errors.py:177\033[0m: Output port _Foo.O not driven
>>         class _Foo(m.Circuit):"""
        assert caplog.records[0].msg == msg
        assert has_error(caplog, msg)
        magma.config.set_debug_mode(False)
