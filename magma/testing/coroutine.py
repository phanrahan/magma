from magma.simulator import PythonSimulator
from hwtypes import BitVector

class Coroutine:
    """
    Makes the initial call to __next__ upon construction to immediately
    start the routine.

    Overrides __getattr__ to support inspection of the local variables
    """
    def __init__(self, *args, **kwargs):
        self.reset(*args, **kwargs)

    @classmethod
    def definition(cls, *args, **kwargs):
        return cls._definition(*args, **kwargs)

    def reset(self, *args, **kwargs):
        self.co = self.definition(*args, **kwargs)
        next(self.co)

    def __getattr__(self, key):
        return self.co.gi_frame.f_locals[key]

    def send(self, args):
        return self.co.send(args)

    def __next__(self):
        return next(self.co)

    def next(self):
        return self.__next__()

def coroutine(func):
    class _Coroutine(Coroutine):
        _definition = func

    return _Coroutine


def check(circuit, sim, number_of_cycles, inputs_generator=None):
    simulator = PythonSimulator(circuit, clock=circuit.CLK)
    failed = False
    for cycle in range(number_of_cycles):
        if inputs_generator is None:
            next(sim)
        else:
            inputs = []
            for name, port in circuit.interface.ports.items():
                if name in ["CLK", "CE"]:
                    continue  # Skip clocks, TODO: Check the type
                if port.is_output():  # circuit input
                    input_value = getattr(inputs_generator, name)
                    inputs.append(input_value)
                    simulator.set_value(getattr(circuit, name), input_value)
            next(inputs_generator)
            if len(inputs) > 1:
                sim.send(inputs)
            elif len(inputs) == 1:
                sim.send(inputs[0])
            else:
                next(sim)
        simulator.advance(2)
        # Coroutine has an implicit __next__ call on construction so it already
        # is in it's initial state
        for name, port in circuit.interface.ports.items():
            if port.is_input():  # circuit output
                if getattr(sim, name) != BitVector(simulator.get_value(getattr(circuit, name))):
                    print(f"Failed on cycle {cycle}, port {name}, expected {getattr(sim, name)}, got {BitVector(simulator.get_value(getattr(circuit, name)))}")
                    failed = True
    assert not failed, "Failed to pass simulation"

def testvectors(circuit, sim, number_of_cycles, inputs_generator=None):
    outputs = []
    inputs = []
    for cycle in range(number_of_cycles):
        next_inputs = []
        in_ports = {}
        if inputs_generator is not None:
            for name, port in circuit.interface.ports.items():
                if name in ["CLK", "CE"]:
                    continue  # Skip clocks, TODO: Check the type
                if port.is_output():  # circuit input
                    input_value = getattr(inputs_generator, name)
                    next_inputs.append(input_value)
                    in_ports[name] = input_value
            next(inputs_generator)
        if len(next_inputs) > 1:
            sim.send(next_inputs)
        elif len(next_inputs) == 1:
            sim.send(next_inputs[0])
        else:
            next(sim)
        out_ports = {}
        for name, port in circuit.interface.ports.items():
            if name == "CLK":
                continue
            if port.is_input():  # circuit output
                out_ports[name] = getattr(sim, name)
        outputs.append(out_ports)
        inputs.append(in_ports)
    return inputs, outputs
