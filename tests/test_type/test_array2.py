import pytest

import magma as m
from magma.testing import check_files_equal


def _check_compile(name, circ, nested=False, inline=False):
    if nested:
        name += "_nested"
    m.compile(f"build/{name}", circ, inline=inline)
    assert check_files_equal(__file__, f"build/{name}.v", f"gold/{name}.v")


@pytest.mark.parametrize('nested', [False, True])
def test_array2_basic(nested):
    class Foo(m.Circuit):
        T = m.Array[2, m.Bit]
        if nested:
            T = m.Array[2, T]
        io = m.IO(I=m.In(T), O=m.Out(T))
        io.O @= io.I

    _check_compile("test_array2_basic", Foo, nested)


@pytest.mark.parametrize('nested', [False, True])
def test_array2_getitem_index(nested):
    class Foo(m.Circuit):
        T = m.Array[2, m.Bit]
        if nested:
            T = m.Array[2, T]
        io = m.IO(I=m.In(T), O=m.Out(T))
        io.O @= m.concat(io.I[1:], io.I[:1])

    _check_compile("test_array2_getitem_index", Foo, nested)


@pytest.mark.parametrize('nested', [False, True])
def test_array2_getitem_slice(nested):
    class Foo(m.Circuit):
        T = m.Array[4, m.Bit]
        if nested:
            T = m.Array[4, T]
        io = m.IO(I=m.In(T), O=m.Out(T))
        io.O @= m.concat(io.I[2:], io.I[:2])

    _check_compile("test_array2_getitem_slice", Foo, nested)


@pytest.mark.parametrize('nested', [False, True])
def test_array2_wire_to_index(nested):
    class Foo(m.Circuit):
        T = m.Array[2, m.Bit]
        if nested:
            T = m.Array[2, T]
        io = m.IO(I=m.In(T), O=m.Out(T))
        io.O[0] @= io.I[1]
        io.O[1] @= io.I[0]

    _check_compile("test_array2_wire_to_index", Foo, nested)


@pytest.mark.parametrize('nested', [False, True])
def test_array2_wire_to_slice(nested):
    class Foo(m.Circuit):
        T = m.Array[4, m.Bit]
        if nested:
            T = m.Array[4, T]
        io = m.IO(I=m.In(T), O=m.Out(T))
        io.O[:2] @= io.I[2:]
        io.O[2:] @= io.I[:2]

    _check_compile("test_array2_wire_to_slice", Foo, nested)


def test_array2_tuple():
    class Foo(m.Circuit):
        T = m.Array[4, m.Tuple[m.Bit, m.Bits[2]]]
        io = m.IO(I=m.In(T),
                  O0=m.Out(T),
                  O1=m.Out(T),
                  O2=m.Out(T),
                  O3=m.Out(T))
        io.O0 @= io.I

        io.O1 @= m.concat(io.I[2:], io.I[:2])

        io.O2[0] @= io.I[1]
        io.O2[1] @= io.I[0]
        io.O2[2] @= io.I[3]
        io.O2[3] @= io.I[2]

        io.O3[:2] @= io.I[2:]
        io.O3[2:] @= io.I[:2]

    _check_compile("test_array2_tuple", Foo)


def test_tuple_array2():
    class Foo(m.Circuit):
        T = m.Tuple[m.Bit, m.Array[2, m.Bit]]
        io = m.IO(I=m.In(T),
                  O=m.Out(T))
        io.O[0] @= io.I[0]
        io.O[1][1] @= io.I[1][0]
        io.O[1][0] @= io.I[1][1]

    _check_compile("test_tuple_array2", Foo)


def test_array2_incremental_child_wire():
    class Foo(m.Circuit):
        T = m.Array[4, m.Tuple[m.Bit, m.Bits[2]]]
        io = m.IO(I=m.In(T), O=m.Out(T))
        for i in range(4):
            io.O[i][0] @= io.I[3 - i][0]
            io.O[i][1] @= io.I[i][1]

    _check_compile("test_array2_incremental_child_wire", Foo)


@pytest.mark.parametrize('nested', [False, True])
def test_array2_getitem_slice_of_slice(nested):
    class Foo(m.Circuit):
        T = m.Array[4, m.Bit]
        if nested:
            T = m.Array[4, T]
        io = m.IO(I=m.In(T), O=m.Out(T))
        io.O @= m.concat(io.I[1:][:2],
                         io.I[:3][1:])

    _check_compile("test_array2_getitem_slice_of_slice", Foo, nested)


@pytest.mark.parametrize('nested', [False, True])
def test_array2_getitem_index_of_slice(nested):
    class Foo(m.Circuit):
        T = m.Array[2, m.Bit]
        if nested:
            T = m.Array[2, T]
        io = m.IO(I=m.In(T), O=m.Out(T))
        io.O[0] @= io.I[1:][0]
        io.O[1] @= io.I[:1][0]

    _check_compile("test_array2_getitem_index_of_slice", Foo, nested)


@pytest.mark.parametrize('nested', [False, True])
def test_array2_getitem_index_of_slice(nested):
    class Foo(m.Circuit):
        T = m.Array[2, m.Bit]
        if nested:
            T = m.Array[2, T]
        io = m.IO(I=m.In(T), O=m.Out(T))
        io.O[0] @= io.I[1:][0]
        io.O[1] @= io.I[:1][0]

    _check_compile("test_array2_getitem_index_of_slice", Foo, nested)


@pytest.mark.parametrize('nested', [False, True])
def test_array2_overlapping_index(nested, caplog):
    class Foo(m.Circuit):
        T = m.Array[2, m.Bit]
        if nested:
            T = m.Array[2, T]
        io = m.IO(I=m.In(T), O=m.Out(T))
        io.O[0] @= io.I[1]
        io.O[0] @= io.I[0]
        io.O[1] @= io.I[0]

    _check_compile("test_array2_overlapping_index", Foo, nested)
    assert (str(caplog.records[0].msg) == "Wiring multiple outputs to same "
                                          "wire, using last connection. Input: "
                                          "Foo.O[0], Old Output: Foo.I[1], "
                                          "New Output: Foo.I[0]")


@pytest.mark.parametrize('nested', [False, True])
def test_array2_overlapping_index_slice(nested, caplog):
    class Foo(m.Circuit):
        T = m.Array[2, m.Bit]
        if nested:
            T = m.Array[2, T]
        io = m.IO(I=m.In(T), O=m.Out(T))
        io.O[0] @= io.I[1]
        io.O[0:2] @= io.I

    _check_compile("test_array2_overlapping_index_slice", Foo, nested)
    assert (str(caplog.records[0].msg) == "Wiring multiple outputs to same "
                                          "wire, using last connection. Input: "
                                          "Foo.O[0], Old Output: Foo.I[1], "
                                          "New Output: Foo.I[0]")


@pytest.mark.parametrize('nested', [False, True])
def test_array2_overlapping_slice_index(nested, caplog):
    class Foo(m.Circuit):
        T = m.Array[2, m.Bit]
        if nested:
            T = m.Array[2, T]
        io = m.IO(I=m.In(T), O=m.Out(T))
        io.O[0:2] @= io.I
        io.O[0] @= io.I[1]

    _check_compile("test_array2_overlapping_slice_index", Foo, nested)
    assert (str(caplog.records[0].msg) == "Wiring multiple outputs to same "
                                          "wire, using last connection. Input: "
                                          "Foo.O[0], Old Output: Foo.I[0], "
                                          "New Output: Foo.I[1]")


@pytest.mark.parametrize('nested', [False, True])
def test_array2_overlapping_slice_slice(nested, caplog):
    class Foo(m.Circuit):
        T = m.Array[4, m.Bit]
        if nested:
            T = m.Array[4, T]
        io = m.IO(I=m.In(T), O=m.Out(T))
        io.O[0:3] @= io.I[1:]
        io.O[1:4] @= io.I[:3]

    _check_compile("test_array2_overlapping_slice_slice", Foo, nested)
    assert (str(caplog.records[0].msg) == "Wiring multiple outputs to same "
                                          "wire, using last connection. Input: "
                                          "Foo.O[1], Old Output: Foo.I[2], "
                                          "New Output: Foo.I[0]")
    assert (str(caplog.records[1].msg) == "Wiring multiple outputs to same "
                                          "wire, using last connection. Input: "
                                          "Foo.O[2], Old Output: Foo.I[3], "
                                          "New Output: Foo.I[1]")


@pytest.mark.parametrize('nested', [False, True])
def test_array2_overlapping_slice_slice2(nested, caplog):
    class Foo(m.Circuit):
        T = m.Array[4, m.Bit]
        if nested:
            T = m.Array[4, T]
        io = m.IO(I=m.In(T), O=m.Out(T))
        io.O[1:4] @= io.I[:3]
        io.O[0:3] @= io.I[1:]

    _check_compile("test_array2_overlapping_slice_slice2", Foo, nested)
    assert (str(caplog.records[0].msg) == "Wiring multiple outputs to same "
                                          "wire, using last connection. Input: "
                                          "Foo.O[1], Old Output: Foo.I[0], "
                                          "New Output: Foo.I[2]")
    assert (str(caplog.records[1].msg) == "Wiring multiple outputs to same "
                                          "wire, using last connection. Input: "
                                          "Foo.O[2], Old Output: Foo.I[1], "
                                          "New Output: Foo.I[3]")


@pytest.mark.parametrize('nested', [False, True])
def test_array2_overlapping_slice_slice3(nested, caplog):
    class Foo(m.Circuit):
        T = m.Array[4, m.Bit]
        if nested:
            T = m.Array[4, T]
        io = m.IO(I=m.In(T), O=m.Out(T))
        # Using overlapping slice with same start index should not infinitely
        # recurse (covers old bug in remove slice logic)
        io.O[0:3] @= io.I[1:]
        io.O[1:3] @= io.I[1:3]
        io.O[3] @= io.I[0]


@pytest.mark.parametrize('nested', [False, True])
def test_array2_overlapping_delayed_slice_index(nested, caplog):
    class Foo(m.Circuit):
        T = m.Array[4, m.Bit]
        if nested:
            T = m.Array[4, T]
        io = m.IO(I=m.In(T), O=m.Out(T))
        x = io.O[1:4]
        io.O[0] @= io.I[1]
        io.O[1] @= io.I[2]
        x @= io.I[:3]

    _check_compile("test_array2_overlapping_delayed_slice_index", Foo, nested)
    assert (str(caplog.records[0].msg) == "Wiring multiple outputs to same "
                                          "wire, using last connection. Input: "
                                          "Foo.O[1], Old Output: Foo.I[2], "
                                          "New Output: Foo.I[0]")


@pytest.mark.parametrize('nested', [False, True])
def test_array2_overlapping_delayed_slice_slice(nested, caplog):
    class Foo(m.Circuit):
        T = m.Array[4, m.Bit]
        if nested:
            T = m.Array[4, T]
        io = m.IO(I=m.In(T), O=m.Out(T))
        x = io.O[1:4]
        io.O[0:2] @= io.I[0:2]
        x @= io.I[:3]

    _check_compile("test_array2_overlapping_delayed_slice_slice", Foo, nested)
    assert (str(caplog.records[0].msg) == "Wiring multiple outputs to same "
                                          "wire, using last connection. Input: "
                                          "Foo.O[1], Old Output: Foo.I[1], "
                                          "New Output: Foo.I[0]")


@pytest.mark.parametrize('nested', [False, True])
def test_array2_overlapping_override_bulk_wire(nested, caplog):
    class Foo(m.Circuit):
        T = m.Array[4, m.Bit]
        if nested:
            T = m.Array[4, T]
        io = m.IO(I=m.In(T), O=m.Out(T))
        io.O @= io.I
        io.O[0] @= io.I[2]

    _check_compile("test_array2_overlapping_override_bulk_wire", Foo, nested)
    assert (str(caplog.records[0].msg) == "Wiring multiple outputs to same "
                                          "wire, using last connection. Input: "
                                          "Foo.O[0], Old Output: Foo.I[0], "
                                          "New Output: Foo.I[2]")


@pytest.mark.parametrize('nested', [False, True])
def test_array2_overlapping_override_bulk_wire_slice(nested, caplog):
    class Foo(m.Circuit):
        T = m.Array[4, m.Bit]
        if nested:
            T = m.Array[4, T]
        io = m.IO(I=m.In(T), O=m.Out(T))
        io.O @= io.I
        io.O[0:2] @= io.I[2:4]

    _check_compile("test_array2_overlapping_override_bulk_wire_slice", Foo,
                   nested)
    error_msg = "Wiring multiple outputs to same wire, using last connection. Input: Foo.O[0], Old Output: Foo.I[0], New Output: Foo.I[2]"  # noqa
    assert str(caplog.records[0].msg) == error_msg


@pytest.mark.parametrize('nested', [False, True])
def test_array2_overlapping_override_bulk_wire2(nested, caplog):
    class Foo(m.Circuit):
        T = m.Array[4, m.Bit]
        if nested:
            T = m.Array[4, T]
        io = m.IO(I=m.In(T), O=m.Out(T))
        io.O @= io.I
        io.O[0] @= io.I[2]
        io.O @= io.I

    _check_compile("test_array2_overlapping_override_bulk_wire2", Foo, nested)


def test_array2_reversed():
    T = m.Array[4, m.Bit]

    class Foo(m.Circuit):
        io = m.IO(I=m.In(T), O=m.Out(T))
        io.O @= io.I[::-1]

    _check_compile("test_array2_reversed", Foo, False)


def test_array2_variable_step_slice():
    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Array[4, m.Bit]), O=m.Out(m.Array[2, m.Bit]))
        io.O @= io.I[1:4:2]

    _check_compile("test_array2_variable_step_slice", Foo, False)


def test_array2_nested_bits_temporary():
    class Foo(m.Circuit):
        io = m.IO(write_pointer=m.In(m.Bits[8]), O=m.Out(m.Array[4, m.Bits[8]]))
        reg = m.Register(m.Bits[8])()
        reg.I @= io.write_pointer
        pointer = m.Array[4, m.Bits[8]](name="pointer")
        x = []
        for i in range(4):
            x.append(m.uint(reg.O) + i)
        pointer @= m.array(x)
        io.O @= pointer
        for i in range(4):
            x = pointer[i][-1] & m.bit(1)

    _check_compile("test_array2_nested_bits_temporary", Foo, False, True)


def test_array2_wire_to_anon():
    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bits[8]), O=m.Out(m.Bits[10]))
        x = m.concat(io.I, m.bits([0, 0]))
        io.O @= x
        for i, driving in enumerate(io.I.driving()):
            assert len(driving) == 1
            assert driving[0] is io.O[i]


def test_array2_unwire():
    S = m.Bits[32]
    T = m.Array[1, S]
    s = S(name="s")
    t = T(name="t")
    s[:] @= t[0]
    assert s.value() is t[0]
    s.unwire(s.value())


def test_array2_unwire2():
    S = m.Bits[32]
    T = m.Array[2, m.Bits[16]]
    s = S(name="s")
    t = T(name="t")
    s[:16] @= t[0]
    s[16:] @= t[1]
    assert all(map(lambda x: x[0] is x[1], zip(s.value(),
                                               t.flatten())))
    s.unwire(s.value())


def test_array2_unwire3():
    S = m.Bits[4]
    T = m.Array[2, m.Bits[2]]
    s = S(name="s")
    t = T(name="t")
    s[0] @= t[0][1]
    s[1] @= t[1][1]
    s[2] @= t[0][0]
    s[3] @= t[1][0]
    expected = [t[0][1], t[1][1], t[0][0], t[1][0]]
    assert all(map(lambda x: x[0] is x[1], zip(s.value(), expected)))
    s.unwire(s.value())


def test_mixed_direction_slice(caplog):
    class T(m.Product):
        x = m.In(m.Bit)
        y = m.Out(m.Bit)

    class Foo(m.Circuit):
        io = m.IO(I=m.Array[4, T], O=m.Array[4, m.Flip(T)])
        io.O[:2] @= io.I[2:]
        io.O[2:] @= io.I[:2]

    assert not caplog.records, "Should not report an error"
    _check_compile("test_array2_mixed_direction_slice", Foo, False,
                   True)


def test_slice_instref(caplog):
    class Bar(m.Circuit):
        io = m.IO(I=m.In(m.Array[2, m.Bit]), O=m.Out(m.Array[2, m.Bit]))

    class Foo(m.Circuit):
        T = m.Array[4, m.Bit]
        io = m.IO(I=m.In(T), O=m.Out(T))
        bar = Bar()
        bar.I @= io.I[2:]
        io.O[2:] @= bar.O
        io.O[:2] @= bar.O
        assert io.O.value().driven() is False
        for i, elem in enumerate(io.O.value()):
            assert isinstance(elem.name, m.ref.ArrayRef)
            assert elem.name.index == i % 2
            assert isinstance(elem.name.array.name, m.ref.InstRef)
            assert elem.name.array.name.inst is bar


def test_array2_2d_tuple():
    class X(m.Product):
        a = m.Array[4, m.Bits[4]]

    class Y(m.Product):
        c = m.Array[2, X]

    class Foo(m.Circuit):
        io = m.IO(I=m.In(Y), O=m.Out(Y))
        io.O @= io.I

        temp = Y()

        for i in range(4):
            temp.c[0].a[3 - i] @= io.I.c[1].a[i]
            temp.c[1].a[i] @= io.I.c[0].a[3 - i]
        io.O @= temp

    expected = """\
Foo = DefineCircuit("Foo", "I", Tuple(c=Array[(2, X)]), "O", Tuple(c=Array[(2, X)]))
wire(Foo.I.c[1].a[3], Foo.O.c[0].a[0])
wire(Foo.I.c[1].a[2], Foo.O.c[0].a[1])
wire(Foo.I.c[1].a[1], Foo.O.c[0].a[2])
wire(Foo.I.c[1].a[0], Foo.O.c[0].a[3])
wire(Foo.I.c[0].a[3], Foo.O.c[1].a[0])
wire(Foo.I.c[0].a[2], Foo.O.c[1].a[1])
wire(Foo.I.c[0].a[1], Foo.O.c[1].a[2])
wire(Foo.I.c[0].a[0], Foo.O.c[1].a[3])
EndCircuit()\
"""
    assert repr(Foo) == expected, repr(Foo)

    _check_compile("test_array2_2d_tuple", Foo, False)


def test_array2_wire_bits_temp():
    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bits[4]), O=m.Out(m.Bits[4]))

        tmp = m.Bits[4]()
        for i in range(4):
            io.O[i] @= tmp[i] ^ io.I[i]

        tmp @= io.I


def test_array2_driving():
    class Foo(m.Circuit):
        T = m.Bits[8]
        io = m.IO(I=m.In(T), O=m.Out(T))
        io.O @= io.I

    class Top(m.Circuit):
        T = Foo.T
        io = m.IO(I=m.In(T), O=m.Out(T))
        out = Foo(name="foo")(io.I)

        x = out[:4] & io.I[4:]
        and_inst = x.name.inst

        y = ~out
        not_inst = y.name.inst

        io.O @= y | m.zext_to(x, 8)

        for i, driving in enumerate(out.driving()):
            assert len(driving) >= 1
            assert driving[-1] is not_inst.I[i]
            if i < 4:
                assert len(driving) == 2
                assert driving[0] is and_inst.I0[i]
            else:
                assert len(driving) == 1
