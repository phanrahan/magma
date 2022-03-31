from functools import wraps, partial
import operator
import pytest
import magma as m
from magma.smart import SmartBit, SmartBits, concat, signed, make_smart
from magma.testing import check_files_equal


def _run_test(func=None, *, skip_check=False):
    if func is None:
        return partial(_run_test, skip_check=skip_check)

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


@_run_test
def test_binop():
    # Ops can be add, sub, mul, div, mod, and, or, xor.
    op = operator.add

    class _Test(m.Circuit):
        io = m.IO(
            I0=m.In(SmartBits[8]),
            I1=m.In(SmartBits[12]),
            O1=m.Out(SmartBits[8]),
            O2=m.Out(SmartBits[12]),
            O3=m.Out(SmartBits[16]))
        val = op(io.I0, io.I1)
        io.O1 @= val
        io.O2 @= val
        io.O3 @= val

    return _Test


@_run_test
def test_comparison():
    # Ops can be eq, ne, ge, gt, le, lt.
    op = operator.eq

    class _Test(m.Circuit):
        io = m.IO(
            I0=m.In(SmartBits[8]),
            I1=m.In(SmartBits[12]),
            O1=m.Out(SmartBits[1]),
            O2=m.Out(SmartBits[16]))
        val = op(io.I0, io.I1)
        io.O1 @= val
        io.O2 @= val

    return _Test


@_run_test
def test_lshift():

    class _Test(m.Circuit):
        io = m.IO(
            I0=m.In(SmartBits[8]),
            I1=m.In(SmartBits[4]),
            O1=m.Out(SmartBits[8]),
            O2=m.Out(SmartBits[16]))
        val = io.I0 << io.I1
        io.O1 @= val
        io.O2 @= val

    return _Test


@_run_test
def test_rshift():

    class _Test(m.Circuit):
        io = m.IO(
            I0=m.In(SmartBits[8]),
            I1=m.In(SmartBits[4]),
            O1=m.Out(SmartBits[4]),
            O2=m.Out(SmartBits[8]),
            O3=m.Out(SmartBits[16]))
        val = io.I0 >> io.I1
        io.O1 @= val
        io.O2 @= val
        io.O3 @= val

    return _Test


@_run_test
def test_concat():

    class _Test(m.Circuit):
        io = m.IO(
            I0=m.In(SmartBits[8]),
            I1=m.In(SmartBits[4]),
            I2=m.In(SmartBits[10]),
            O1=m.Out(SmartBits[4]),
            O2=m.Out(SmartBits[16]))
        val = concat(io.I0 + io.I1, io.I2)
        io.O1 @= val
        io.O2 @= val

    return _Test


@_run_test
def test_unary():
    # Ops can be invert, neg.
    op = operator.invert

    class _Test(m.Circuit):
        io = m.IO(
            I0=m.In(SmartBits[8]),
            O1=m.Out(SmartBits[4]),
            O2=m.Out(SmartBits[16]))
        val = op(io.I0)
        io.O1 @= val
        io.O2 @= val

    return _Test


@_run_test
def test_reduction():
    # Ops can be and, or, xor.
    op = operator.and_

    class _Test(m.Circuit):
        io = m.IO(
            I0=m.In(SmartBits[8]),
            O1=m.Out(SmartBits[1]),
            O2=m.Out(SmartBits[16]))
        val = io.I0.reduce(op)
        io.O1 @= val
        io.O2 @= val

    return _Test


@_run_test
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
                T = SmartBit if width is None else SmartBits[width]
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
            out @= concat(x, y, z)  # extend concat; width = 10 + 16 + 1 = 27.


    class _TestTop(m.Circuit):
        inst = _Test(name="Test")

    return type(_TestTop.instances[0])


@_run_test
def test_complex():

    class _Test(m.Circuit):
        io = m.IO(
            I0=m.In(SmartBits[7]),
            I1=m.In(SmartBits[9, True]),
            I2=m.In(SmartBits[12, True]),
            O=m.Out(SmartBits[10]),
            O2=m.Out(SmartBits[7]),
            O3=m.Out(SmartBit),
        )

        x = (~(io.I0 + io.I1) + io.I2) << io.I0.reduce(operator.and_)
        y = signed(io.I1 <= io.I2) + signed(io.I0)

        io.O @= x
        io.O2 @= y
        io.O3 @= io.I0

    EXPECTED = ("lshift(add(invert(add(Extend[width=5, "
                "signed=False](SmartBits[7, False](I0)), Extend[width=3, "
                "signed=False](SmartBits[9, True](I1)))), SmartBits[12, "
                "True](I2)), Extend[width=11, "
                "signed=False](AndReduce(SmartBits[7, False](I0))))")
    assert str(_Test.io.O._smart_expr_) == EXPECTED

    return _Test


def test_type_constructors():
    T1 = SmartBits[8]
    assert T1._T is m.Bits[8]
    assert T1._signed == False

    T2 = SmartBits[12, True]
    assert T2._T is m.Bits[12]
    assert T2._signed == True

    with pytest.raises(TypeError) as pytest_e:
        T3 = SmartBits[8][12]
        assert False
    args = pytest_e.value.args
    assert args == ("Can not doubly qualify SmartBits, i.e. "
                    "SmartBits[n][m] not allowed",)


@_run_test(skip_check=True)
def test_unsigned_add():
    class _Test(m.Circuit):
        io = m.IO(
            x=m.In(SmartBits[8, True]),
            y=m.In(SmartBits[16, False]),
            O=m.Out(SmartBits[20, True])
        )
        io.O @= io.x + io.y

    return _Test


def test_make_smart():

    class _T(m.Product):
        x = m.Bits[8]
        y = m.Array[10, m.Bits[16]]

    # Value should be non-anonymous so that the value checks below work.
    value = _T(name="value")
    smart = make_smart(value)

    # Type checks.
    assert isinstance(smart, m.Tuple)
    assert set(type(smart).field_dict.keys()) == {"x", "y"}
    assert isinstance(smart.x, SmartBits)
    assert len(smart.x) == 8 and type(smart.x)._signed == False
    assert isinstance(smart.y, m.Array)
    assert isinstance(smart.y[0], SmartBits)
    assert len(smart.y[0]) == 16
    assert type(smart.y[0])._signed == False

    # Value checks.
    assert smart.x._get_magma_value_() is value.x
    for i in range(10):
        assert smart.y[i]._get_magma_value_() is value.y[i]
