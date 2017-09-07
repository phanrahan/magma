from magma import In, Out, Flip, \
    Clock, ClockType, ClockKind, \
    Reset, ResetType, ResetKind, \
    Enable, EnableType, EnableKind

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
