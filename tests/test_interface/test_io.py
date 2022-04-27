import pytest

import magma as m


def _io_similar(lhs: m.IO, rhs: m.IO) -> bool:
    """
    Returns True if @lhs and @rhs have the same signature, false otherwise. Note
    that this does not check the identity of the underlying ports, just their
    names and types. That is, the following holds

        args = dict(...)
        x = IO(**args)
        y = IO(**args)
        assert _io_similar(x, y)
    """
    ldecl = lhs.decl()
    rdecl = rhs.decl()
    if not ldecl[::2] == rdecl[::2]:  # names are the same
        return False
    size = len(ldecl)
    return all(ldecl[i] is rdecl[i] for i in range(1, size, 2))


def test_basic():
    expected_names = ["y", "x"]
    expected_types = [m.In(m.Bit), m.Out(m.Bits[8])]
    io = m.IO(y=m.In(m.Bit), x=m.Out(m.Bits[8]))
    assert list(io.ports.keys()) == expected_names
    ports = list(io.ports.values())
    assert all(type(ports[i]) is expected_types[i].flip() for i in range(2))
    assert all(io.decl()[i*2+1] is expected_types[i] for i in range(2))
    assert io.decl()[::2] == expected_names
    for port in io.ports.values():
        assert isinstance(port.name, m.DefnRef)


def test_bind(caplog):
    io = m.IO(y=m.In(m.Bit), x=m.Out(m.Bits[8]))

    class _Foo(m.Circuit):
        pass

    io.bind(_Foo)
    for port in io.ports.values():
        assert isinstance(port.name, m.DefnRef)
        assert port.name.defn is _Foo

    # Check that calling bind() again throws an exception.
    with pytest.raises(Exception) as pytest_e:
        io.bind(_Foo)
        assert False
    assert pytest_e.type is Exception
    assert pytest_e.value.args == ("Can not bind IO multiple times",)


def test_add():
    x = m.IO(x=m.In(m.Bit))
    y = m.IO(y=m.In(m.Bit))
    z = x + y
    expected = m.IO(x=m.In(m.Bit), y=m.In(m.Bit))
    assert _io_similar(z, expected)
    # Check that x and y haven't changed.
    assert _io_similar(x, m.IO(x=m.In(m.Bit)))
    assert _io_similar(y, m.IO(y=m.In(m.Bit)))


def test_add_non_io():
    x = m.IO(x=m.In(m.Bit))
    with pytest.raises(TypeError) as pytest_e:
        z = x + 0  # try adding another type to IO
        assert False
    assert pytest_e.type is TypeError
    assert (
        pytest_e.value.args ==
        ("unsupported operand type(s) for +: 'IO' and 'int'",)
    )


def test_add_bound_io(caplog):

    class _Foo(m.Circuit):
        io = m.IO(x=m.In(m.Bit))

    y = m.IO(y=m.In(m.Bit))
    with pytest.raises(Exception) as pytest_e:
        z = _Foo.io + y
        assert False
    assert pytest_e.type is Exception
    assert pytest_e.value.args == ("Adding bound IO not allowed",)


def test_add_intersecting_io(caplog):
    x = m.IO(x=m.In(m.Bit))
    x_again = m.IO(x=m.In(m.Bit))
    with pytest.raises(Exception) as pytest_e:
        z = x + x_again
        assert False
    assert pytest_e.type is Exception
    assert pytest_e.value.args == (
        "Adding IO with duplicate port names not allowed",
    )


def test_flip():
    A = m.Product.from_fields("anon", dict(x=m.In(m.Bit), y=m.Out(m.Bit)))
    B = m.In(m.Bits[8])
    io = m.IO(a=A, b=B)
    flipped = io.flip()
    # Check flipped io.
    assert flipped.fields() == {"a": A.flip(), "b": B.flip()}
    # Check that flip(flip) = id.
    assert flipped.flip().fields() == io.fields()


def test_getitem():
    io = m.IO(a=m.In(m.Bit))
    assert io.a is io["a"]
