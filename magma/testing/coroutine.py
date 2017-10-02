from magma.simulator import PythonSimulator
from magma.bit_vector import BitVector

def coroutine(func):
    class Coroutine:
        """
        Makes the initial call to __next__ upon construction to immediately
        start the routine.

        Overrides __getattr__ to support inspection of the local variables
        """
        def __init__(self, *args, **kwargs):
            self.definition = func
            self.reset(*args, **kwargs)

        def reset(self, *args, **kwargs):
            self.co = self.definition(*args, **kwargs)
            next(self.co)

        def __getattr__(self, key):
            return self.co.gi_frame.f_locals[key]

        def send(self, *args, **kwargs):
            return self.co.send(*args, **kwargs)

        def __next__(self):
            return next(self.co)

        def next(self):
            return self.__next__()

    return Coroutine


def check(circuit, sim, number_of_cycles):
    simulator = PythonSimulator(circuit, clock=circuit.CLK)
    for cycle in range(number_of_cycles):
        for i in range(2):
            simulator.step()
            simulator.evaluate()
        # Coroutine has an implicit __next__ call on construction so it already
        # is init it's initial state
        assert sim.O == BitVector(simulator.get_value(circuit.O)).as_int()
        next(sim)
