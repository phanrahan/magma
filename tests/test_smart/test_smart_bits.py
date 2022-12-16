from functools import wraps, partial
import operator
import pytest

import magma as m
from magma.testing import check_files_equal


def _run_repr_test(func):

    @wraps(func)
    def _wrapper(*args, **kwargs):
        test_ckt, gold_ckt = func(*args, **kwargs)
        test_lines = repr(test_ckt).split("\n")[1:]
        gold_lines = repr(gold_ckt).split("\n")[1:]
        assert test_lines == gold_lines

    return _wrapper


def _run_compilation_test(func=None, *, skip_check=False):
    if func is None:
        return partial(_run_compilation_test, skip_check=skip_check)

    @wraps(func)
    def _wrapper(*args, **kwargs):
        name = func.__name__
        ckt = func(*args, **kwargs)
        m.compile(f"build/{name}", ckt, output="coreir-verilog", inline=True)
        build = f"build/{name}.v"
        gold = f"gold/{name}.v"
        if not skip_check:
            assert check_files_equal(__file__, build, gold)

    return _wrapper


@pytest.mark.parametrize(
    "op",
    (
        operator.add,
        operator.sub,
        operator.mul,
        operator.floordiv,
        operator.mod,
        operator.and_,
        operator.or_,
        operator.xor,
    )
)
@_run_repr_test
def test_binop(op):

    class _Test(m.Circuit):
        name = "test_binop"
        io = m.IO(
            I0=m.In(m.smart.SmartBits[8]),
            I1=m.In(m.smart.SmartBits[12]),
            O1=m.Out(m.smart.SmartBits[8]),
            O2=m.Out(m.smart.SmartBits[12]),
            O3=m.Out(m.smart.SmartBits[16]))
        val = op(io.I0, io.I1)
        io.O1 @= val
        io.O2 @= val
        io.O3 @= val

    class _Gold(m.Circuit):
        name = "test_binop"
        io = m.IO(
            I0=m.In(m.UInt[8]),
            I1=m.In(m.UInt[12]),
            O1=m.Out(m.UInt[8]),
            O2=m.Out(m.UInt[12]),
            O3=m.Out(m.UInt[16]))
        O1 = m.UInt[8]()
        O1 @= op(m.zext_to(io.I0, 12), io.I1)[:8]
        O1[0]  # force elaboration for repr test
        io.O1 @= O1
        io.O2 @= op(m.zext_to(io.I0, 12), io.I1)
        io.O3 @= op(m.zext_to(io.I0, 16), m.zext_to(io.I1, 16))

    return _Test, _Gold


@_run_repr_test
def test_comparison():
    # Ops can be eq, ne, ge, gt, le, lt.
    op = operator.gt

    class _Test(m.Circuit):
        name = "test_comparison"
        io = m.IO(
            I0=m.In(m.smart.SmartBits[8]),
            I1=m.In(m.smart.SmartBits[12]),
            O1=m.Out(m.smart.SmartBits[1]),
            O2=m.Out(m.smart.SmartBits[16]))
        val = op(io.I0, io.I1)
        io.O1 @= val
        io.O2 @= val

    class _Gold(m.Circuit):
        name = "test_comparison"
        io = m.IO(
            I0=m.In(m.UInt[8]),
            I1=m.In(m.UInt[12]),
            O1=m.Out(m.UInt[1]),
            O2=m.Out(m.UInt[16]))
        io.O1 @= m.bits(op(m.zext_to(io.I0, 12), io.I1))
        io.O2 @= m.zext_to(m.bits(op(m.zext_to(io.I0, 12), m.zext_to(io.I1, 12))), 16)

    return _Test, _Gold


@_run_repr_test
def test_lshift():

    class _Test(m.Circuit):
        name = "test_lshift"
        io = m.IO(
            I0=m.In(m.smart.SmartBits[8]),
            I1=m.In(m.smart.SmartBits[4]),
            O1=m.Out(m.smart.SmartBits[8]),
            O2=m.Out(m.smart.SmartBits[16]))
        val = io.I0 << io.I1
        io.O1 @= val
        io.O2 @= val

    class _Gold(m.Circuit):
        name = "test_lshift"
        io = m.IO(
            I0=m.In(m.UInt[8]),
            I1=m.In(m.UInt[4]),
            O1=m.Out(m.UInt[8]),
            O2=m.Out(m.UInt[16]))
        io.O1 @= io.I0 << m.zext_to(io.I1, 8)
        O2 = m.UInt[16]()
        O2 @= m.zext_to(io.I0 << m.zext_to(io.I1, 8), 16)
        io.O2 @= O2

    return _Test, _Gold


@_run_repr_test
def test_rshift():

    class _Test(m.Circuit):
        name = "test_rshift"
        io = m.IO(
            I0=m.In(m.smart.SmartBits[8]),
            I1=m.In(m.smart.SmartBits[4]),
            O1=m.Out(m.smart.SmartBits[4]),
            O2=m.Out(m.smart.SmartBits[8]),
            O3=m.Out(m.smart.SmartBits[16]))
        val = io.I0 >> io.I1
        io.O1 @= val
        io.O2 @= val
        io.O3 @= val

    class _Gold(m.Circuit):
        name = "test_rshift"
        io = m.IO(
            I0=m.In(m.UInt[8]),
            I1=m.In(m.UInt[4]),
            O1=m.Out(m.UInt[4]),
            O2=m.Out(m.UInt[8]),
            O3=m.Out(m.UInt[16]))
        O1 = m.UInt[4]()
        O1 @= (io.I0 >> m.zext_to(io.I1, 8))[:4]
        O1[0]  # force elaboration for repr test
        io.O1 @= O1
        io.O2 @= m.zext_to(io.I0 >> m.zext_to(io.I1, 8), 8)
        O3 = m.UInt[16]()
        O3 @= m.zext_to(io.I0 >> m.zext_to(io.I1, 8), 16)
        io.O3 @= O3

    return _Test, _Gold


@_run_repr_test
def test_concat():

    class _Test(m.Circuit):
        name = "test_concat"
        io = m.IO(
            I0=m.In(m.smart.SmartBits[8]),
            I1=m.In(m.smart.SmartBits[4]),
            I2=m.In(m.smart.SmartBits[10]),
            O1=m.Out(m.smart.SmartBits[4]),
            O2=m.Out(m.smart.SmartBits[16]))
        val = m.smart.concat(io.I0 + io.I1, io.I2)
        io.O1 @= val
        io.O2 @= val

    class _Gold(m.Circuit):
        name = "test_concat"
        io = m.IO(
            I0=m.In(m.UInt[8]),
            I1=m.In(m.UInt[4]),
            I2=m.In(m.UInt[10]),
            O1=m.Out(m.UInt[4]),
            O2=m.Out(m.UInt[16]))
        O1 = m.UInt[4]()
        O1 @= m.concat(io.I0 + m.zext_to(io.I1, 8), io.I2)[:4]
        io.O1 @= O1
        O2 = m.UInt[16]()
        O2 @= m.concat(io.I0 + m.zext_to(io.I1, 8), io.I2)[:16]
        io.O2 @= O2

    return _Test, _Gold


@_run_repr_test
def test_repeat():

    class _Test(m.Circuit):
        name = "test_repeat"
        io = m.IO(
            I0=m.In(m.smart.SmartBits[8]),
            I1=m.In(m.smart.SmartBits[4]),
            O1=m.Out(m.smart.SmartBits[24]),
            O2=m.Out(m.smart.SmartBits[6]),
        )
        io.O1 @= m.smart.repeat(io.I0, 3)
        io.O2 @= m.smart.repeat(io.I1[0], 6)

    class _Gold(m.Circuit):
        name = "test_repeat"
        io = m.IO(
            I0=m.In(m.UInt[8]),
            I1=m.In(m.UInt[4]),
            O1=m.Out(m.UInt[24]),
            O2=m.Out(m.UInt[6]),
        )
        O1 = m.UInt[24]()  # force elaboration for repr test
        O1 @= m.as_bits(m.repeat(io.I0, 3))
        O2 = m.UInt[6]()  # force elaboration for repr test
        O2 @= m.repeat(io.I1[0], 6)
        io.O1 @= O1
        io.O2 @= O2

    return _Test, _Gold


@_run_repr_test
def test_unary():
    # Ops can be invert, neg.
    op = operator.invert

    class _Test(m.Circuit):
        name = "test_unary"
        io = m.IO(
            I0=m.In(m.smart.SmartBits[8]),
            O1=m.Out(m.smart.SmartBits[4]),
            O2=m.Out(m.smart.SmartBits[16]))
        val = op(io.I0)
        io.O1 @= val
        io.O2 @= val

    class _Gold(m.Circuit):
        name = "test_unary"
        io = m.IO(
            I0=m.In(m.UInt[8]),
            O1=m.Out(m.UInt[4]),
            O2=m.Out(m.UInt[16]))
        O1 = m.UInt[4]()
        O1 @= op(io.I0)[:4]
        O1[0]  # force elaboration for repr test
        io.O1 @= O1
        io.O2 @= op(m.zext_to(io.I0, 16))

    return _Test, _Gold


@_run_repr_test
def test_reduction():
    # Ops can be and, or, xor.
    op = operator.and_

    class _Test(m.Circuit):
        name = "test_reduction"
        io = m.IO(
            I0=m.In(m.smart.SmartBits[8]),
            O1=m.Out(m.smart.SmartBits[1]),
            O2=m.Out(m.smart.SmartBits[16]))
        val = io.I0.reduce(op)
        io.O1 @= val
        io.O2 @= val

    class _Gold(m.Circuit):
        name = "test_reduction"
        io = m.IO(
            I0=m.In(m.UInt[8]),
            O1=m.Out(m.UInt[1]),
            O2=m.Out(m.UInt[16]))
        io.O1 @= m.bits(m.reduce(op, io.I0))
        io.O2 @= m.zext_to(m.bits(m.reduce(op, io.I0)), 16)

    return _Test, _Gold


@_run_repr_test
def test_slice():

    class _Test(m.Circuit):
        name = "test_slice"
        io = m.IO(
            I0=m.In(m.smart.SmartBits[8]),
            O0=m.Out(m.smart.SmartBits[12]),
            O1=m.Out(m.smart.SmartBits[12]),
        )
        io.O0 @= io.I0[2:6]
        io.O1 @= io.I0[2]

    class _Gold(m.Circuit):
        name = "test_slice"
        io = m.IO(
            I0=m.In(m.UInt[8]),
            O0=m.Out(m.UInt[12]),
            O1=m.Out(m.UInt[12]),
        )
        io.O0 @= m.zext_to(io.I0[2:6], 12)
        io.O1 @= m.zext_to(m.bits(io.I0[2]), 12)

    return _Test, _Gold


@_run_compilation_test
def test_smoke():

    # NOTE(rsetaluri): We use a CircuitBuilder here just so we can dynamically
    # add ports to make the test specification easier. The test just creates a
    # bunch of SmartBits values and does operations and wires them. This is
    # easiest to do and check in the context of a circuit definition. It is also
    # (mostly) possible to do them on anonymous values but is less convenient.

    class _Test(m.CircuitBuilder):
        def __init__(self, name):
            super().__init__(name)
            self._counter = 0

        def fresh_name(self):
            name = f"port{self._counter}"
            self._counter += 1
            return name

        def make_ports(self, *widths):
            assert len(widths) >= 2
            names = []
            for i, width in enumerate(widths):
                name = self.fresh_name()
                width = widths[i]
                T = m.smart.SmartBit if width is None else m.smart.SmartBits[width]
                dir_ = m.Out if i == 0 else m.In
                self._add_port(name, dir_(T))
                names.append(name)
            return [self._port(name) for name in names]

        @m.builder_method
        def _finalize(self):
            # Any Smart<x> can be wired to any Smart<y>.
            x, y = self.make_ports(10, 16)
            x @= y  # truncate y
            y, x = self.make_ports(16, 10)
            y @= x  # extend x
            x, z = self.make_ports(10, None)
            x @= z  # extend z
            z, x = self.make_ports(None, 10)
            z @= x  # truncate x

            # Any Smart<x> (op) Smart<y> is valid; each (op) has its own width
            # rules.

            # Arithmetic and logic.
            out, x, y = self.make_ports(12, 10, 16)
            out @= x + y  # width = max(12, 10, 16); op: +, -, *, /, %, &, |, ^
            out, x, z = self.make_ports(None, 10, None)
            out @= x + z  # width = max(1, 10, 1)
            out, x = self.make_ports(16, 10)
            out @= ~x  # width = max(16, 10); ~

            # Comparison.
            out, x, y = self.make_ports(12, 10, 16)
            out @= x <= y  # width = 1; op: ==, !=, <, <=, >, >=

            # Reductiton.
            out, x = self.make_ports(4, 10)
            out @= x.reduce(operator.and_)  # width = 1; op: &, |, ^

            # Shifting.
            out, x, y = self.make_ports(10, 10, 16)
            out @= x << y  # extend x, truncate output; width = 10; op: <<, >>
            out, x, y = self.make_ports(16, 10, 16)
            out @=  y << x  # extend x; width = 16
            out, x, z = self.make_ports(10, 10, None)
            out @= x << z  # extend z; width = 10
            out, x, z = self.make_ports(None, 10, None)
            out @= z << x  # extend z, truncate output; width = 1

            # Concat.
            out, x, y, z = self.make_ports(32, 10, 16, None)
            out @= m.smart.concat(x, y, z)  # extend concat; width = 10 + 16 + 1 = 27.


    class _TestTop(m.Circuit):
        inst = _Test(name="Test")

    return type(_TestTop.instances[0])


@_run_compilation_test
def test_complex():

    class _Test(m.Circuit):
        io = m.IO(
            I0=m.In(m.smart.SmartBits[7]),
            I1=m.In(m.smart.SmartBits[9, True]),
            I2=m.In(m.smart.SmartBits[12, True]),
            O=m.Out(m.smart.SmartBits[10]),
            O2=m.Out(m.smart.SmartBits[7]),
            O3=m.Out(m.smart.SmartBit),
        )

        x = (~(io.I0 + io.I1) + io.I2) << io.I0.reduce(operator.and_)
        y = m.smart.signed(io.I1 <= io.I2) + m.smart.signed(io.I0)

        io.O @= x
        io.O2 @= y
        io.O3 @= io.I0

    return _Test


def test_type_constructors():
    T1 = m.smart.SmartBits[8]
    assert T1._T_ is m.Bits[8]
    assert T1._signed_ == False

    T2 = m.smart.SmartBits[12, True]
    assert T2._T_ is m.Bits[12]
    assert T2._signed_ == True

    with pytest.raises(TypeError) as pytest_e:
        T3 = m.smart.SmartBits[8][12]
        assert False
    args = pytest_e.value.args
    assert args == ("Can not doubly qualify SmartBits",)


@_run_compilation_test(skip_check=True)
def test_unsigned_add():
    class _Test(m.Circuit):
        io = m.IO(
            x=m.In(m.smart.SmartBits[8, True]),
            y=m.In(m.smart.SmartBits[16, False]),
            O=m.Out(m.smart.SmartBits[20, True])
        )
        io.O @= io.x + io.y

    return _Test


def test_type():
    assert m.smart.SmartBits[32] == m.smart.SmartBits[32]
    assert m.smart.SmartBits[32] == m.smart.SmartBits[32].qualify(m.Direction.Undirected)
    assert m.smart.SmartBits[32] != m.smart.SmartBits[33]
    # NOTE(rsetaluri): We noticed a bug where, due to equality not being defined
    # on SmartBitsMeta, constructing Products containing SmartBit's failed
    # (subclass check resulted in non-terminating recursion).


def test_make_smart():

    class _T(m.Product):
        x = m.Bits[8]
        y = m.Array[10, m.Bits[16]]

    # Value should be non-anonymous so that the value checks below work.
    value = _T(name="value")
    smart = m.smart.make_smart(value)

    # Type checks.
    assert isinstance(smart, m.Tuple)
    assert set(type(smart).field_dict.keys()) == {"x", "y"}
    assert isinstance(smart.x, m.smart.SmartBits)
    assert len(smart.x) == 8 and type(smart.x)._signed_ == False
    assert isinstance(smart.y, m.Array)
    assert isinstance(smart.y[0], m.smart.SmartBits)
    assert len(smart.y[0]) == 16
    assert type(smart.y[0])._signed_ == False

    # Value checks.
    assert smart.x._get_magma_value_() is value.x
    for i in range(10):
        assert smart.y[i]._get_magma_value_() is value.y[i]


@_run_repr_test
def test_eval():

    class _Test(m.Circuit):
        name = "test_eval"
        io = m.IO(
            I0=m.In(m.smart.SmartBits[8]),
            I1=m.In(m.smart.SmartBits[12]),
            O0=m.Out(m.smart.SmartBits[16])
        )
        O0 = m.smart.SmartBits[16]()
        O0 @= io.I0 + io.I1
        io.O0 @= O0

    class _Gold(m.Circuit):
        name = "test_eval"
        io = m.IO(
            I0=m.In(m.smart.SmartBits[8]),
            I1=m.In(m.smart.SmartBits[12]),
            O0=m.Out(m.smart.SmartBits[16])
        )
        O0 = m.smart.SmartBits[16]()
        O0 @= m.smart.evaluate(io.I0 + io.I1, 16)
        io.O0 @= O0

    return _Test, _Gold


@_run_repr_test
def test_mux():

    class _Test(m.Circuit):
        name = "test_mux"
        io = m.IO(
            I0=m.In(m.smart.SmartBits[8]),
            I1=m.In(m.smart.SmartBits[12]),
            S=m.In(m.smart.SmartBits[8]),
            O0=m.Out(m.smart.SmartBits[16]),
        )
        io.O0 @= m.smart.mux([io.I0, io.I1], io.S)

    class _Gold(m.Circuit):
        name = "test_mux"
        io = m.IO(
            I0=m.In(m.UInt[8]),
            I1=m.In(m.UInt[12]),
            S=m.In(m.UInt[8]),
            O0=m.Out(m.UInt[16]),
        )
        O0 = m.UInt[16]()  # force elaboration for repr test
        O0 @= m.zext_to(m.mux([m.zext_to(io.I0, 12), io.I1], io.S[0]), 16)
        io.O0 @= O0

    return _Test, _Gold
