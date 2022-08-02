import pytest

import magma as m
from magma.testing import check_files_equal
from magma.types.handshake import ReadyValidException


@pytest.mark.parametrize('T', [m.ReadyValid, m.Decoupled, m.Irrevocable])
def test_ready_valid_simple(T):
    class TestReadyValidSimple(m.Circuit):
        io = m.IO(
            I=m.Consumer(T[m.Bits[5]]),
            O=m.Producer(T[m.Bits[5]]),
            fired=m.Out(m.Bit)
        )
        assert isinstance(io.I, T)
        assert isinstance(io.I, T[m.Bits[5]])
        # Flipped because defn view
        assert m.is_producer(type(io.I))
        assert m.is_consumer(type(io.O))
        assert m.is_producer(io.I)
        assert m.is_consumer(io.O)
        io.O @= io.I
        io.fired @= io.I.fired() & io.O.fired()

    m.compile("build/TestReadyValidSimple", TestReadyValidSimple, inline=True)
    assert check_files_equal(__file__, "build/TestReadyValidSimple.v",
                             "gold/TestReadyValidSimple.v")


@pytest.mark.parametrize('T', [m.ReadyValid, m.Decoupled, m.Irrevocable])
def test_ready_valid_tuple(T):
    class TestReadyValidTuple(m.Circuit):
        io = m.IO(
            I=m.Consumer(T[m.Tuple[m.Bit, m.Bits[5]]]),
            O=m.Producer(T[m.Tuple[m.Bit, m.Bits[5]]])
        )
        io.O @= io.I

    m.compile("build/TestReadyValidTuple", TestReadyValidTuple)
    assert check_files_equal(__file__, "build/TestReadyValidTuple.v",
                             "gold/TestReadyValidTuple.v")


@pytest.mark.parametrize('T', [m.ReadyValid, m.Decoupled, m.Irrevocable])
def test_ready_valid_when(T):
    class TestReadyValidWhen(m.Circuit):
        io = m.IO(
            I=m.Consumer(T[m.Bits[5]]),
            O=m.Producer(T[m.Bits[5]])
        )
        # Default no enq/deq
        io.O.no_enq()
        io.I.no_deq()

        data = io.I.deq(when=io.I.valid)
        io.O.enq(data, when=io.I.valid)

    m.compile("build/TestReadyValidWhen", TestReadyValidWhen, inline=True)
    assert check_files_equal(__file__, "build/TestReadyValidWhen.v",
                             "gold/TestReadyValidWhen.v")


@pytest.mark.parametrize('T', [m.ReadyValid, m.Decoupled, m.Irrevocable])
def test_ready_valid_no_enq_when(T):
    class TestReadyValidNoEnqWhen(m.Circuit):
        io = m.IO(
            I=m.In(m.Bit),
            O=m.Producer(T[m.Bits[5]])
        )
        io.O.enq(m.Bits[5](0x1E))
        io.O.no_enq(when=io.I)

    m.compile("build/TestReadyValidNoEnqWhen", TestReadyValidNoEnqWhen,
              inline=True)
    assert check_files_equal(__file__, "build/TestReadyValidNoEnqWhen.v",
                             "gold/TestReadyValidNoEnqWhen.v")


@pytest.mark.parametrize('T', [m.ReadyValid, m.Decoupled, m.Irrevocable])
def test_ready_valid_no_deq_when(T):
    class TestReadyValidNoDeqWhen(m.Circuit):
        io = m.IO(
            I0=m.In(m.Bit),
            I1=m.Consumer(T[m.Bits[5]]),
            O=m.Out(m.Bits[5])
        )
        io.O @= io.I1.deq()
        io.I1.no_deq(when=io.I0)

    m.compile("build/TestReadyValidNoDeqWhen", TestReadyValidNoDeqWhen,
              inline=True)
    assert check_files_equal(__file__, "build/TestReadyValidNoDeqWhen.v",
                             "gold/TestReadyValidNoDeqWhen.v")


@pytest.mark.parametrize('T', [m.ReadyValid, m.Decoupled, m.Irrevocable])
def test_ready_valid_warnings(T, caplog):
    T[m.In(m.Bit)]
    assert caplog.messages[0] == """\
Type In(Bit) used with ReadyValid is not undirected, converting to undirected\
 type\
"""


@pytest.mark.parametrize('T', [m.ReadyValid, m.Decoupled, m.Irrevocable])
def test_ready_valid_errors(T):
    # TypeError on invalid type param
    with pytest.raises(TypeError):
        T[1]

    # Cannot use produce/consume on non-ready/valid
    # TODO: We could use Producer/Consumer as a convenience wrapper for
    # creating ReadyValid[T] with the desired polarity
    with pytest.raises(TypeError):
        m.Consumer(m.Bit)
    with pytest.raises(TypeError):
        m.Producer(m.Bit)

    class TestReadyValidErrors(m.Circuit):
        io = m.IO(
            I=m.Consumer(T[m.Bits[5]]),
            O=m.Producer(T[m.Bits[5]]),
            fired=m.Out(m.Bit)
        )
        # Cannot call fired when valid or ready is not wired yet
        with pytest.raises(ReadyValidException):
            io.I.fired()
        with pytest.raises(ReadyValidException):
            io.O.fired()

        # Cannot call enq/deq on invalid direction
        with pytest.raises(AttributeError):
            io.I.enq(None)
        with pytest.raises(AttributeError):
            io.I.no_enq()
        with pytest.raises(AttributeError):
            io.O.deq()
        with pytest.raises(AttributeError):
            io.O.no_deq()

        # cannot use deq/enq when without default
        with pytest.raises(ReadyValidException):
            io.I.deq(when=io.O.ready)
        with pytest.raises(ReadyValidException):
            io.O.enq(io.I.data, when=io.I.valid)


def test_enq_deq_io(caplog):
    class Main(m.Circuit):
        T1 = m.EnqIO[m.Bits[5]]
        T2 = m.Producer(m.Decoupled[m.Bits[5]])
        assert T1 == T2
        v1, v2 = T1(), T2()
        # Should not error when wiring
        v1 @= v2
        assert len(caplog.messages) == 0

        T3 = m.DeqIO[m.Bits[5]]
        T4 = m.Consumer(m.Decoupled[m.Bits[5]])
        assert T3 == T4
        v3, v4 = T3(), T4()
        # Should not error when wiring
        v3 @= v4
        assert len(caplog.messages) == 0


def test_flip_ready_valid():
    T = m.Bits[5]

    class StubQueue(m.Circuit):
        # Queues have a flipped interface since it's from the perspective of
        # the user
        io = m.IO(
            enq=m.Flip(m.EnqIO[T]),
            deq=m.Flip(m.DeqIO[T]),
        )
        print(f"type(io.deq)={type(io.deq)}")
        print(f"type(io.enq)={type(io.enq)}")

        io.deq.valid @= 0
        io.enq.ready @= 0

        do_enq = io.enq.fired()
        do_deq = io.deq.fired()

        io.deq.data @= io.enq.data


def test_ready_valid_none():
    assert (m.ReadyValid[None].qualify(m.Direction.Undirected) is
            m.ReadyValid[None])

    class Foo(m.Circuit):
        io = m.IO(producer_handshake=m.Producer(m.ReadyValid[None]),
                  consumer_handshake=m.Consumer(m.ReadyValid[None]))
        io.producer_handshake.valid @= io.producer_handshake.ready ^ 1
        io.consumer_handshake.ready @= io.consumer_handshake.valid ^ 1

        assert type(io.producer_handshake).undirected_data_t is None
        assert type(io.consumer_handshake).undirected_data_t is None
        assert not hasattr(io.producer_handshake, "data")
        assert not hasattr(io.consumer_handshake, "data")
        with pytest.raises(Exception):
            io.producer_handshake.enq(1)
        with pytest.raises(Exception):
            io.producer_handshake.no_enq(1)
        with pytest.raises(Exception):
            io.consumer_handshake.deq()
        with pytest.raises(Exception):
            io.consumer_handshake.no_deq(1)
    m.compile("build/Foo", Foo)


@pytest.mark.parametrize("qualifiers", [
    (m.Consumer, m.Producer, m.In, lambda x: x.undirected_t, m.Out)
])
def test_qualify_ready_valid(qualifiers):
    T = m.ReadyValid[m.Bits[8]]

    for q in qualifiers:
        T = q(T)
        assert issubclass(T, m.ReadyValid[m.Bits[8]])
        if q in (m.Producer, m.Consumer, m.In, m.Out):
            T = T.flip()
            assert issubclass(T, m.ReadyValid[m.Bits[8]])
        else:
            msg = (
                f"Cannot flip {T.__name__} (undirected)")
            with pytest.raises(TypeError) as e:
                T.flip()
            assert str(e.value) == msg


def test_credit_valid():
    x = m.CreditValid[m.Bits[8]]
    assert hasattr(x, "credit")
    assert m.Producer(x) is m.Consumer(x).flip()
