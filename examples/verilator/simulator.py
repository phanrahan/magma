from itertools import product
from magma import BitType, ArrayType
from magma.python_simulator import PythonSimulator, Scope

__all__ = ['testvectors']

def testvectors(circuit, mode='complete'):

    simulator = PythonSimulator(circuit)
    scope = Scope()

    args = []
    for name, port in circuit.interface.ports.items():
        if port.isoutput():
            if isinstance(port, BitType):
                if name != 'CLK':
                    args.append([0,1])
            else:
                assert False

    tests = []
    for test in product(*args):

        # set inputs
        i = 0
        for name, port in circuit.interface.ports.items():
            if port.isoutput() and name != 'CLK':
                simulator.set_value(port, scope, bool(test[i]))
                i += 1

        simulator.evaluate()

        # get values
        t = []
        for name, port in circuit.interface.ports.items():
            if name != 'CLK':
                t.append( simulator.get_value(port, scope) )

        tests.append(t)

    return tests

