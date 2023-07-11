import magma as m


def test_fold_shift_register(caplog):
    # https://github.com/phanrahan/magma/issues/808
    class EnableShiftRegister(m.Circuit):
        io = m.IO(
            I=m.In(m.UInt[4]),
            shift=m.In(m.Enable),
            O=m.Out(m.UInt[4])
        ) + m.ClockIO(has_async_reset=True)
        regs = [m.Register(m.UInt[4], reset_type=m.AsyncReset,
                           has_enable=True)() for _ in range(4)]
        io.O @= m.fold(regs, foldargs={"I": "O"},
                       forkargs=["CE"])(io.I, CE=io.shift)

    m.compile("build/EnableShiftRegister", EnableShiftRegister)

    assert "Wiring multiple outputs to same wire, using last connection. Input: EnableShiftRegister.Register_inst0.CLK, Old Output: Clock(), New Output: EnableShiftRegister.CLK" not in caplog.messages  # noqa
    assert 'Wiring multiple outputs to same wire, using last connection. Input: EnableShiftRegister.Register_inst0.ASYNCRESET, Old Output: AsyncReset(), New Output: EnableShiftRegister.ASYNCRESET' not in caplog.messages  # noqa


def test_fold_reset_shift_register():
    # https://github.com/phanrahan/magma/issues/816
    class ResetShiftRegister(m.Circuit):
        io = m.IO(
            I=m.In(m.UInt[4]),
            shift=m.In(m.Enable),
            O=m.Out(m.UInt[4])
        ) + m.ClockIO(has_resetn=True)
        regs = [m.Register(m.UInt[4], has_enable=True, reset_type=m.ResetN)()
                for _ in range(4)]
        io.O @= m.fold(regs, foldargs={"I": "O"},
                       forkargs=["CE"])(io.I, CE=io.shift)

    # This should not raise an unconnected port exception
    m.compile("build/ResetShiftRegister", ResetShiftRegister)
