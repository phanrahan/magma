from magma import *
from magma.simulator import PythonSimulator

def test_instance():
    N = 4
    T = Bits[N]

    class Test(Circuit):
        name = "Test"
        IO = ["I", In(T), "O", Out(T), "CLK", In(Bit)]
        @classmethod
        def definition(io):
            wire(io.I, io.O)

    try:
        simulator = PythonSimulator(Test())
        assert False, "Should raise a ValueError when passing an instance to the Python Simulator"
    except ValueError as e:
        pass
