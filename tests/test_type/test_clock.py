import tempfile
import pytest
import magma as m
from magma.testing import check_files_equal
from magma import In, Out, Flip, \
    Clock, \
    Reset, reset, \
    Enable, enable, \
    AsyncReset, \
    DeclareCircuit, DefineCircuit, EndCircuit, \
    Bit, bit, wire, compile

from magma.digital import DigitalMeta


def test_clock():
    assert isinstance(Clock, DigitalMeta)
    assert Clock == Clock
    assert not (Clock != Clock)
    assert str(Clock) == 'Clock'

    assert issubclass(m.Clock, m.Digital)
    assert isinstance(m.Clock(), m.Digital)

    assert issubclass(m.Clock, m.Digital)
    assert isinstance(m.Clock(), m.Digital)

    assert issubclass(m.In(m.Clock), In(m.Digital))
    assert isinstance(m.In(m.Clock)(), In(m.Digital))

    assert not issubclass(m.In(m.Clock), Out(m.Digital))
    assert not isinstance(m.In(m.Clock)(), Out(m.Digital))

    assert issubclass(m.In(m.Clock), m.Clock)
    assert isinstance(m.In(m.Clock)(), m.Clock)

    assert not issubclass(m.In(m.Clock), m.Out(m.Clock))
    assert not isinstance(m.In(m.Clock)(), m.Out(m.Clock))

    assert issubclass(m.Out(m.Clock), Out(m.Digital))
    assert isinstance(m.Out(m.Clock)(), Out(m.Digital))

    assert not issubclass(m.Out(m.Clock), In(m.Digital))
    assert not isinstance(m.Out(m.Clock)(), In(m.Digital))

    assert issubclass(m.Out(m.Clock), m.Clock)
    assert isinstance(m.Out(m.Clock)(), m.Clock)

    assert not issubclass(m.Out(m.Clock), m.In(m.Clock))
    assert not isinstance(m.Out(m.Clock)(), m.In(m.Clock))


def test_clock_flip():
    ClockOut = Out(Clock)
    assert issubclass(ClockOut, Clock)
    assert str(ClockOut) == 'Out(Clock)'

    ClockIn = In(Clock)
    assert issubclass(ClockIn, Clock)
    assert str(ClockIn) == 'In(Clock)'

    clockin = In(ClockIn)
    clockout = Out(ClockIn)
    assert clockout == ClockOut
    assert clockin == ClockIn

    clockin = In(ClockOut)
    clockout = Out(ClockOut)
    assert clockout == ClockOut
    assert clockin == ClockIn

    clockin = Flip(ClockOut)
    clockout = Flip(ClockIn)
    assert clockout == ClockOut
    assert clockin == ClockIn


def test_clock_val():
    b = Clock(name="a")
    assert str(b) == "a"
    assert isinstance(b, Clock)
    assert not b.is_input()
    assert not b.is_output()


def test_reset():
    assert isinstance(Reset, DigitalMeta)
    assert Reset == Reset
    assert not (Reset != Reset)
    assert str(Reset) == 'Reset'

    assert issubclass(m.In(m.Reset), In(m.Digital))
    assert isinstance(m.In(m.Reset)(), In(m.Digital))

    assert not issubclass(m.In(m.Reset), Out(m.Digital))
    assert not isinstance(m.In(m.Reset)(), Out(m.Digital))

    assert issubclass(m.In(m.Reset), m.Reset)
    assert isinstance(m.In(m.Reset)(), m.Reset)

    assert not issubclass(m.In(m.Reset), m.Out(m.Reset))
    assert not isinstance(m.In(m.Reset)(), m.Out(m.Reset))

    assert issubclass(m.Out(m.Reset), Out(m.Digital))
    assert isinstance(m.Out(m.Reset)(), Out(m.Digital))

    assert not issubclass(m.Out(m.Reset), In(m.Digital))
    assert not isinstance(m.Out(m.Reset)(), In(m.Digital))

    assert issubclass(m.Out(m.Reset), m.Reset)
    assert isinstance(m.Out(m.Reset)(), m.Reset)

    assert not issubclass(m.Out(m.Reset), m.In(m.Reset))
    assert not isinstance(m.Out(m.Reset)(), m.In(m.Reset))

    assert issubclass(m.ResetN, m.Digital)
    assert isinstance(m.ResetN(), m.Digital)

    assert issubclass(m.ResetN, m.Digital)
    assert isinstance(m.ResetN(), m.Digital)

    assert issubclass(m.In(m.ResetN), In(m.Digital))
    assert isinstance(m.In(m.ResetN)(), In(m.Digital))

    assert not issubclass(m.In(m.ResetN), Out(m.Digital))
    assert not isinstance(m.In(m.ResetN)(), Out(m.Digital))

    assert issubclass(m.In(m.ResetN), m.ResetN)
    assert isinstance(m.In(m.ResetN)(), m.ResetN)

    assert not issubclass(m.In(m.ResetN), m.Out(m.ResetN))
    assert not isinstance(m.In(m.ResetN)(), m.Out(m.ResetN))

    assert issubclass(m.Out(m.ResetN), Out(m.Digital))
    assert isinstance(m.Out(m.ResetN)(), Out(m.Digital))

    assert not issubclass(m.Out(m.ResetN), In(m.Digital))
    assert not isinstance(m.Out(m.ResetN)(), In(m.Digital))

    assert issubclass(m.Out(m.ResetN), m.ResetN)
    assert isinstance(m.Out(m.ResetN)(), m.ResetN)

    assert not issubclass(m.Out(m.ResetN), m.In(m.ResetN))
    assert not isinstance(m.Out(m.ResetN)(), m.In(m.ResetN))

    assert issubclass(m.AsyncReset, m.Digital)
    assert isinstance(m.AsyncReset(), m.Digital)

    assert issubclass(m.AsyncReset, m.Digital)
    assert isinstance(m.AsyncReset(), m.Digital)

    assert issubclass(m.In(m.AsyncReset), In(m.Digital))
    assert isinstance(m.In(m.AsyncReset)(), In(m.Digital))

    assert not issubclass(m.In(m.AsyncReset), Out(m.Digital))
    assert not isinstance(m.In(m.AsyncReset)(), Out(m.Digital))

    assert issubclass(m.In(m.AsyncReset), m.AsyncReset)
    assert isinstance(m.In(m.AsyncReset)(), m.AsyncReset)

    assert not issubclass(m.In(m.AsyncReset), m.Out(m.AsyncReset))
    assert not isinstance(m.In(m.AsyncReset)(), m.Out(m.AsyncReset))

    assert issubclass(m.Out(m.AsyncReset), Out(m.Digital))
    assert isinstance(m.Out(m.AsyncReset)(), Out(m.Digital))

    assert not issubclass(m.Out(m.AsyncReset), In(m.Digital))
    assert not isinstance(m.Out(m.AsyncReset)(), In(m.Digital))

    assert issubclass(m.Out(m.AsyncReset), m.AsyncReset)
    assert isinstance(m.Out(m.AsyncReset)(), m.AsyncReset)

    assert not issubclass(m.Out(m.AsyncReset), m.In(m.AsyncReset))
    assert not isinstance(m.Out(m.AsyncReset)(), m.In(m.AsyncReset))

    assert issubclass(m.AsyncResetN, m.Digital)
    assert isinstance(m.AsyncResetN(), m.Digital)

    assert issubclass(m.AsyncResetN, m.Digital)
    assert isinstance(m.AsyncResetN(), m.Digital)

    assert issubclass(m.In(m.AsyncResetN), In(m.Digital))
    assert isinstance(m.In(m.AsyncResetN)(), In(m.Digital))

    assert not issubclass(m.In(m.AsyncResetN), Out(m.Digital))
    assert not isinstance(m.In(m.AsyncResetN)(), Out(m.Digital))

    assert issubclass(m.In(m.AsyncResetN), m.AsyncResetN)
    assert isinstance(m.In(m.AsyncResetN)(), m.AsyncResetN)

    assert not issubclass(m.In(m.AsyncResetN), m.Out(m.AsyncResetN))
    assert not isinstance(m.In(m.AsyncResetN)(), m.Out(m.AsyncResetN))

    assert issubclass(m.Out(m.AsyncResetN), Out(m.Digital))
    assert isinstance(m.Out(m.AsyncResetN)(), Out(m.Digital))

    assert not issubclass(m.Out(m.AsyncResetN), In(m.Digital))
    assert not isinstance(m.Out(m.AsyncResetN)(), In(m.Digital))

    assert issubclass(m.Out(m.AsyncResetN), m.AsyncResetN)
    assert isinstance(m.Out(m.AsyncResetN)(), m.AsyncResetN)

    assert not issubclass(m.Out(m.AsyncResetN), m.In(m.AsyncResetN))
    assert not isinstance(m.Out(m.AsyncResetN)(), m.In(m.AsyncResetN))


def test_reset_flip():
    ResetOut = Out(Reset)
    assert issubclass(ResetOut, Reset)
    assert str(ResetOut) == 'Out(Reset)'

    ResetIn = In(Reset)
    assert issubclass(ResetIn, Reset)
    assert str(ResetIn) == 'In(Reset)'

    resetin = In(ResetIn)
    resetout = Out(ResetIn)
    assert resetout == ResetOut
    assert resetin == ResetIn

    resetin = In(ResetOut)
    resetout = Out(ResetOut)
    assert resetout == ResetOut
    assert resetin == ResetIn

    resetin = Flip(ResetOut)
    resetout = Flip(ResetIn)
    assert resetout == ResetOut
    assert resetin == ResetIn


def test_reset_val():
    b = Reset(name="a")
    assert str(b) == "a"
    assert isinstance(b, Reset)
    assert not b.is_input()
    assert not b.is_output()
    assert not b.is_inout()


def test_enable():
    assert isinstance(Enable, DigitalMeta)
    assert Enable == Enable
    assert not (Enable != Enable)
    assert str(Enable) == 'Enable'

    assert issubclass(m.In(m.Enable), In(m.Digital))
    assert isinstance(m.In(m.Enable)(), In(m.Digital))

    assert not issubclass(m.In(m.Enable), Out(m.Digital))
    assert not isinstance(m.In(m.Enable)(), Out(m.Digital))

    assert issubclass(m.In(m.Enable), m.Enable)
    assert isinstance(m.In(m.Enable)(), m.Enable)

    assert not issubclass(m.In(m.Enable), m.Out(m.Enable))
    assert not isinstance(m.In(m.Enable)(), m.Out(m.Enable))

    assert issubclass(m.Out(m.Enable), Out(m.Digital))
    assert isinstance(m.Out(m.Enable)(), Out(m.Digital))

    assert not issubclass(m.Out(m.Enable), In(m.Digital))
    assert not isinstance(m.Out(m.Enable)(), In(m.Digital))

    assert issubclass(m.Out(m.Enable), m.Enable)
    assert isinstance(m.Out(m.Enable)(), m.Enable)

    assert not issubclass(m.Out(m.Enable), m.In(m.Enable))
    assert not isinstance(m.Out(m.Enable)(), m.In(m.Enable))


def test_enable_flip():
    EnableOut = Out(Enable)
    assert issubclass(EnableOut, Enable)
    assert str(EnableOut) == 'Out(Enable)'

    EnableIn = In(Enable)
    assert issubclass(EnableIn, Enable)
    assert str(EnableIn) == 'In(Enable)'

    enablein = In(EnableIn)
    enableout = Out(EnableIn)
    assert enableout == EnableOut
    assert enablein == EnableIn

    enablein = In(EnableOut)
    enableout = Out(EnableOut)
    assert enableout == EnableOut
    assert enablein == EnableIn

    enablein = Flip(EnableOut)
    enableout = Flip(EnableIn)
    assert enableout == EnableOut
    assert enablein == EnableIn


def test_enable_val():
    b = Enable(name="a")
    assert str(b) == "a"
    assert isinstance(b, Enable)
    assert not b.is_input()
    assert not b.is_output()


@pytest.mark.parametrize("T", [Clock, AsyncReset])
def test_coreir_wrap(T):
    def define_wrap(type_, type_name, in_type):
        def sim_wrap(self, value_store, state_store):
            input_val = value_store.get_value(getattr(self, "in"))
            value_store.set_value(self.out, input_val)

        return DeclareCircuit(
            f'coreir_wrap{type_name}',
            "in", In(in_type), "out", Out(type_),
            coreir_genargs={"type": type_},
            coreir_name="wrap",
            coreir_lib="coreir",
            simulate=sim_wrap
        )

    foo = DefineCircuit("foo", "r", In(T))
    EndCircuit()

    top = DefineCircuit("top", "O", Out(Bit))
    foo_inst = foo()
    wrap = define_wrap(T, "Bit", Bit)()
    wire(bit(0), wrap.interface.ports["in"])
    wire(wrap.out, foo_inst.r)
    wire(bit(0), top.O)
    EndCircuit()

    with tempfile.TemporaryDirectory() as tempdir:
        filename = f"{tempdir}/top"
        compile(filename, top, output="coreir")
        got = open(f"{filename}.json").read()
    expected_filename = f"tests/test_type/test_coreir_wrap_golden_{T}.json"
    expected = open(expected_filename).read()
    assert got == expected


@pytest.mark.parametrize("T,t", [(Reset, reset), (Enable, enable)])
def test_const_wire(T, t):
    foo = DefineCircuit("foo", "I", In(T))
    EndCircuit()

    top = DefineCircuit("top", "O", Out(Bit))
    foo_inst = foo()
    wire(t(0), foo_inst.I)
    wire(bit(0), top.O)
    EndCircuit()

    with tempfile.TemporaryDirectory() as tempdir:
        filename = f"{tempdir}/top"
        compile(filename, top, output="coreir")
        got = open(f"{filename}.json").read()
    expected_filename = f"tests/test_type/test_const_wire_golden.json"
    expected = open(expected_filename).read()
    assert got == expected


@pytest.mark.parametrize("T,convert", [(m.AsyncResetOut, m.asyncreset),
                                       (m.AsyncResetNOut, m.asyncresetn)])
def test_asyncreset_cast(T, convert):
    class Inst(m.Circuit):
        io = m.IO(O=T, I=m.In(T))

    class AsyncResetTest(m.Circuit):
        io = m.IO(I=m.BitIn, I_Arr=m.In(m.Array[3, Bit]),
                  O=T, O_Tuple=m.Product.from_fields(
                      "anon", {"R": T, "B": Out(Bit)}),
                  O_Arr=m.Array[2, T],
                  T_in=In(T), Bit_out=Out(Bit),
                  T_Arr_in=In(m.Array[2, T]),
                  T_Tuple_in=In(m.Product.from_fields("anon", {"T": T})),
                  Bit_Arr_out=Out(m.Array[4, Bit]))

        inst = Inst()
        io.O <= convert(io.I)
        io.O_Tuple.R <= convert(io.I_Arr[0])
        io.O_Arr[0] <= convert(io.I_Arr[1])
        io.O_Arr[1] <= convert(io.I_Arr[2])
        inst.I <= convert(io.I_Arr[2])
        io.Bit_out <= m.bit(io.T_in)
        io.O_Tuple.B <= m.bit(io.T_Tuple_in.T)
        io.Bit_Arr_out[0] <= m.bit(io.T_Arr_in[0])
        io.Bit_Arr_out[1] <= m.bit(io.T_Arr_in[1])
        io.Bit_Arr_out[2] <= m.bit(io.T_Arr_in[0])
        io.Bit_Arr_out[3] <= m.bit(inst.O)

    m.compile(f"build/test_{T.__name__}_cast", AsyncResetTest)
    assert check_files_equal(__file__, f"build/test_{T.__name__}_cast.v",
                             f"gold/test_{T.__name__}_cast.v")
