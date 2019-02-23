import magma as m
from test_combinational import compile_and_check, phi
from collections import Sequence


def _RegisterName(name, n, init, ce, r):
    name += str(n)
    if ce:
        name += 'CE'
    if r:
        name += 'R'

    if isinstance(init, Sequence):
        init = seq2int(init)
    if init is not 0:
        name += "_%04X" % init

    return name


def DefineRegister(n, init=0, has_ce=False, has_reset=False,
                   has_async_reset=False, _type=m.Bits):
    """
    Stub for testing
    """
    if _type not in {m.Bits, m.UInt, m.SInt}:
        raise ValueError("Argument _type must be Bits, UInt, or SInt")
    T = _type(n)

    class _Register(m.Circuit):
        name = _RegisterName('Register', n, init, has_ce, has_reset)
        IO = ['I', m.In(T), 'O', m.Out(T)] + \
            m.ClockInterface(has_ce=has_ce, has_reset=has_reset,
                             has_async_reset=has_async_reset)
    return _Register


def Register(n, init=0, has_ce=False, has_reset=False, has_async_reset=False,
             **kwargs):
    return DefineRegister(n, init, has_ce, has_reset,
                          has_async_reset)(**kwargs)


def pytest_generate_tests(metafunc):
    if 'target' in metafunc.fixturenames:
        metafunc.parametrize("target", ["coreir"])


def test_seq_simple(target):
    @m.circuit.sequential
    class Basic:
        def __init__(self):
            self.x: m.Bits(2) = m.bits(0, 2)
            self.y: m.Bits(2) = m.bits(0, 2)

        def __call__(self, I: m.Bits(2)) -> m.Bits(2):
            O = self.y
            self.y = self.x
            self.x = I
            return O

    compile_and_check("test_seq_simple", Basic, target)


def test_seq_hierarchy(target):
    def DefineCustomRegister(width, init=0):
        @m.circuit.sequential
        class Register:
            def __init__(self):
                self.value: m.Bits(width) = m.bits(init, width)

            def __call__(self, I: m.Bits(width)) -> m.Bits(width):
                O = self.value
                self.value = I
                return O

        return Register

    @m.circuit.sequential
    class ShiftRegister:
        def __init__(self):
            # [<exp>] means execute the Python expression during the first
            # stage of compilation

            # The type of a hierarchal output must have the same signature for
            # the input and output (can have a tuple for multiple inputs). This
            # reflects the ability to read and write to the variable with the
            # same meaning

            # Only supported in __init__ body for now
            self.x: m.Bits(2) = [DefineCustomRegister(2, init=0)()]
            self.y: m.Bits(2) = [DefineCustomRegister(2, init=1)()]

        def __call__(self, I: m.Bits(2)) -> m.Bits(2):
            O = self.y
            self.y = self.x
            self.x = I
            return O

    compile_and_check("test_seq_hierarchy", ShiftRegister, target)
