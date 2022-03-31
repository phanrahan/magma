import magma as m
from typing import Dict


def _assert_io_fields(io: m.IO, fields: Dict[str, m.Kind]):
    """Asserts that @io has ordered fields in @fields."""
    for ((name0, T0), (name1, T1)) in zip(io.fields().items(), fields.items()):
        assert name0 == name1
        assert T0 == T1


def test_io_flip():
    A = m.Product.from_fields("anon", dict(x=m.In(m.Bit), y=m.Out(m.Bit)))
    B = m.In(m.Bits[8])
    io = m.IO(a=A, b=B)
    flipped = io.flip()
    # Check flipped io.
    _assert_io_fields(flipped, {"a": A.flip(), "b": B.flip()})
    # Check that flip(flip) = id.
    _assert_io_fields(flipped.flip(), io.fields())
