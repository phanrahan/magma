import pytest

import magma as m
from magma.testing import check_files_equal
from magma.types.decoupled import ReadyValidException


def test_ready_valid_simple():
    class TestReadyValidSimple(m.Circuit):
        io = m.IO(
            I=m.Consume(m.ReadyValid[m.Bits[5]]),
            O=m.Produce(m.ReadyValid[m.Bits[5]]),
            fired=m.Out(m.Bit)
        )
        assert isinstance(io.I, m.ReadyValid)
        io.O @= io.I
        io.fired @= io.I.fired() & io.O.fired()

    m.compile("build/TestReadyValidSimple", TestReadyValidSimple, inline=True)
    assert check_files_equal(__file__, f"build/TestReadyValidSimple.v",
                             f"gold/TestReadyValidSimple.v")


def test_ready_valid_tuple():
    class TestReadyValidTuple(m.Circuit):
        io = m.IO(
            I=m.Consume(m.ReadyValid[m.Tuple[m.Bit, m.Bits[5]]]),
            O=m.Produce(m.ReadyValid[m.Tuple[m.Bit, m.Bits[5]]])
        )
        io.O @= io.I

    m.compile("build/TestReadyValidTuple", TestReadyValidTuple)
    assert check_files_equal(__file__, f"build/TestReadyValidTuple.v",
                             f"gold/TestReadyValidTuple.v")


def test_ready_valid_when():
    class TestReadyValidWhen(m.Circuit):
        io = m.IO(
            I=m.Consume(m.ReadyValid[m.Bits[5]]),
            O=m.Produce(m.ReadyValid[m.Bits[5]])
        )
        # Default no enq/deq
        io.O.no_enq()
        io.I.no_deq()

        data = io.I.deq(when=io.I.valid)
        io.O.enq(data, when=io.I.valid)

    m.compile("build/TestReadyValidWhen", TestReadyValidWhen, inline=True)
    assert check_files_equal(__file__, f"build/TestReadyValidWhen.v",
                             f"gold/TestReadyValidWhen.v")


def test_ready_valid_no_enq_when():
    class TestReadyValidNoEnqWhen(m.Circuit):
        io = m.IO(
            I=m.In(m.Bit),
            O=m.Produce(m.ReadyValid[m.Bits[5]])
        )
        io.O.enq(m.Bits[5](0xDE))
        io.O.no_enq(when=io.I)

    m.compile("build/TestReadyValidNoEnqWhen", TestReadyValidNoEnqWhen,
              inline=True)
    assert check_files_equal(__file__, f"build/TestReadyValidNoEnqWhen.v",
                             f"gold/TestReadyValidNoEnqWhen.v")


def test_ready_valid_no_deq_when():
    class TestReadyValidNoDeqWhen(m.Circuit):
        io = m.IO(
            I0=m.In(m.Bit),
            I1=m.Consume(m.ReadyValid[m.Bits[5]]),
            O=m.Out(m.Bits[5])
        )
        io.O @= io.I1.deq()
        io.I1.no_deq(when=io.I0)

    m.compile("build/TestReadyValidNoDeqWhen", TestReadyValidNoDeqWhen,
              inline=True)
    assert check_files_equal(__file__, f"build/TestReadyValidNoDeqWhen.v",
                             f"gold/TestReadyValidNoDeqWhen.v")


def test_ready_valid_errors():
    # TypeError on invalid type param
    with pytest.raises(TypeError):
        m.ReadyValid[1]

    # Cannot use produce/consume on non-ready/valid
    # TODO: We could use Produce/Consume as a convenience wrapper for creating
    # ReadyValid[T] with the desired polarity
    with pytest.raises(TypeError):
        m.Consume(m.Bit)
    with pytest.raises(TypeError):
        m.Produce(m.Bit)

    class TestReadyValidErrors(m.Circuit):
        io = m.IO(
            I=m.Consume(m.ReadyValid[m.Bits[5]]),
            O=m.Produce(m.ReadyValid[m.Bits[5]]),
            fired=m.Out(m.Bit)
        )
        # Cannot call fired when valid or ready is not wired yet
        with pytest.raises(ReadyValidException):
            io.I.fired()
        with pytest.raises(ReadyValidException):
            io.O.fired()

        # Cannot call enq/deq on invalid direction
        with pytest.raises(TypeError):
            io.I.enq(None)
        with pytest.raises(TypeError):
            io.I.no_enq()
        with pytest.raises(TypeError):
            io.O.deq()
        with pytest.raises(TypeError):
            io.O.no_deq()

        # cannot use deq/enq when without default
        with pytest.raises(ReadyValidException):
            io.I.deq(when=io.O.ready)
        with pytest.raises(ReadyValidException):
            io.O.enq(io.I.data, when=io.I.valid)
