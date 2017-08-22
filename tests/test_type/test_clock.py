from magma import Clock, ClockType, ClockKind, In, Out, Flip

def test_clock():
    assert isinstance(Clock,    ClockKind)
    assert Clock == Clock
    assert str(Clock) == 'Clock'

def test_clock_flip():
    ClockOut = Out(Clock)
    assert isinstance(ClockOut,    ClockKind)
    assert str(ClockOut) == 'Out(Clock)'
    ClockIn = In(Clock)
    assert isinstance(ClockIn,    ClockKind)
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
    assert not b.isinout()
