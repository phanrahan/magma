import magma as m
from magma.smart import SmartBit, SmartBits, concat
from magma.testing import check_files_equal
from functools import wraps, partial
import operator


def _run_test(func=None, *, info=None):
    if func is None:
        return partial(_run_test, info=info)

    @wraps(func)
    def _wrapper(*args, **kwargs):
        name = func.__name__
        ckt = func(*args, **kwargs)
        m.compile(f"build/{name}", ckt, output="coreir-verilog", inline=True)
        build = f"build/{name}.v"
        gold = f"gold/{name}.v"
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


def test_circuit():

    class _Foo(m.Circuit):
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

        print ()
        print ("=======================")
        print (x)
        print (y)
        print (io.I0)
        print ("=======================")

        io.O @= x
        io.O2 @= y
        io.O3 @= io.I0

    #print (repr(_Foo))

    m.compile("Foo", _Foo, output="coreir-verilog", inline=True)


def test_basic():
    def x_():
        return SmartBits[10]()

    def y_():
        return SmartBits[16]()

    def z_():
        return SmartBit()

    class Foo(m.Circuit):

        x = x_()
        y = y_()
        z = z_()

        # Any Smart<x> can be wired to any Smart<y>.
        x @= y  # truncate y
        y @= x  # extend x
        #x @= z  # promote z to SmartBits[1], then extend z
        #z @= x  # promote z to SmartBits[1], then truncate x

        # Any Smart<x> (op) Smart<y> is valid; each (op) has its own width rules.
        # Arithmetic and logic.
        x @= x + y  # out width = max(10, 16) = 16; op is +, -, *, /, %, &, |, ^
        #x + z  # promote z to SmartBits[1]; out width = max(1, 10) = 10
        ~x  # out width = 10; ~
        #~z  # out = SmartBit
        #z + z  # promote *both* z's to SmartBits[1], then extract LSB;
               # out = SmartBit

        # Comparison.
        x <= y  # out = SmartBit; op is ==, !=, <, <=, >, >=, reduction

        # Shifting
        x << y  # extend x, truncate output; out width = 10; op is <<, >>
        y << x  # extend x; out width = 16
        #x << z  # promote z to SmartBits[1], extend z; out width = 10
        #z << x  # promote z to SmartBits[1], extend z, truncate output;
                # out = SmartBit

        # Any (op) Smart<x> is valid (unary op); (op)'s follow simple width rules.
        ~x  # out width = 10
        #~z  # out = SmartBit

        # Context-determined operators.
