import pytest
import tempfile
import magma as m
from magma.testing import check_files_equal
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


@pytest.mark.parametrize("T,convert", [(m.AsyncResetOut, m.asyncreset),
                                       (m.AsyncResetNOut, m.asyncresetn)])
def test_asyncreset_cast(T, convert):
    class Inst(m.Circuit):
        IO = ['O', T, 'I', m.In(T)]

    class AsyncResetTest(m.Circuit):
        IO = ['I', m.BitIn, 'I_Arr', m.In(m.Array[3, Bit]),
              'O', T, "O_Tuple", m.Tuple(R=T, B=Out(Bit)),
              "O_Arr", m.Array[2, T],
              'T_in', In(T), 'Bit_out', Out(Bit),
              'T_Arr_in', In(m.Array[2, T]),
              'Bit_Arr_out', Out(m.Array[3, Bit]),
              'T_Tuple_in', In(m.Tuple(T=T)),
              'Bit_Arr_out', Out(m.Array[4, Bit])]

        @classmethod
        def definition(io):
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
