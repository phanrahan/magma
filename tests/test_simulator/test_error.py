from magma import *
from magma.simulator import PythonSimulator


def test_instance():
    N = 4
    T = Bits[N]

    class Test(Circuit):
        name = "Test"
        io = IO(I=In(T), O=Out(T), CLK=In(Bit))
        wire(io.I, io.O)

    class _Top(Circuit):
        io = IO()
        test = Test()

    try:
        simulator = PythonSimulator(_Top.test)
        assert False, "Should raise a ValueError when passing an instance to the Python Simulator"
    except ValueError as e:
        pass
