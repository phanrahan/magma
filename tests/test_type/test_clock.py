import pytest
import tempfile
from magma import In, Out, Flip, \
    Clock, ClockType, ClockKind, \
    Reset, ResetType, ResetKind, reset, \
    Enable, EnableType, EnableKind, enable, \
    AsyncReset, AsyncResetType, AsyncResetKind, \
    DeclareCircuit, DefineCircuit, EndCircuit, \
    Bit, bit, wire, compile

def test_clock():
    assert isinstance(Clock, ClockKind)
    assert Clock == Clock
    assert str(Clock) == 'Clock'

def test_clock_flip():
    ClockOut = Out(Clock)
    assert isinstance(ClockOut, ClockKind)
    assert str(ClockOut) == 'Out(Clock)'

    ClockIn = In(Clock)
    assert isinstance(ClockIn, ClockKind)
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
    assert isinstance(b, ClockType)
    assert isinstance(b, Clock)
    assert not b.isinput()
    assert not b.isoutput()

def test_reset():
    assert isinstance(Reset, ResetKind)
    assert Reset == Reset
    assert str(Reset) == 'Reset'

def test_reset_flip():
    ResetOut = Out(Reset)
    assert isinstance(ResetOut, ResetKind)
    assert str(ResetOut) == 'Out(Reset)'

    ResetIn = In(Reset)
    assert isinstance(ResetIn, ResetKind)
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
    assert isinstance(b, ResetType)
    assert isinstance(b, Reset)
    assert not b.isinput()
    assert not b.isoutput()
    assert not b.isinout()

def test_enable():
    assert isinstance(Enable, EnableKind)
    assert Enable == Enable
    assert str(Enable) == 'Enable'

def test_enable_flip():
    EnableOut = Out(Enable)
    assert isinstance(EnableOut, EnableKind)
    assert str(EnableOut) == 'Out(Enable)'

    EnableIn = In(Enable)
    assert isinstance(EnableIn, EnableKind)
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
    assert isinstance(b, EnableType)
    assert isinstance(b, Enable)
    assert not b.isinput()
    assert not b.isoutput()

@pytest.mark.parametrize("T", [Clock, AsyncReset])
def test_coreir_wrap(T):
    def define_wrap(type_, type_name, in_type):
        def sim_wrap(self, value_store, state_store):
            input_val = value_store.get_value(getattr(self, "in"))
            value_store.set_value(self.out, input_val)

        return DeclareCircuit(
            f'coreir_wrap{type_name}',
            "in", In(in_type), "out", Out(type_),
            coreir_genargs = {"type": type_},
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
