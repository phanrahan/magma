from magma import BitType, ArrayType
from inspect import signature
from itertools import product

# check that number of function arguments equals number of circuit inputs
def check(circuit, func):
    sig = signature(func)
    nfuncargs = len(sig.parameters)

    # count circuit inputs
    ncircargs = 0
    for name, port in circuit.interface.ports.items():
        if port.isoutput():
            ncircargs += 1
    assert nfuncargs == ncircargs

def testvectors(circuit, func, mode='complete'):
    check(circuit, func)

    args = []
    for name, port in circuit.interface.ports.items():
        if port.isoutput():
            if isinstance(port, BitType):
                args.append([False,True])
            elif isinstance(port, ArrayType):
                args.append(range(1<<type(port).N))
            else:
                assert True, "can't test Tuples"

    nargs = len(args)
    tests = []
    for test in product(*args):
         test = list(test)
         tests.append(test+[func(*test)])

    return tests
