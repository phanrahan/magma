from magma import BitType, ArrayType
from magma.bit_vector import BitVector
import sys
if sys.version_info < (3, 3):
    from funcsigs import signature
else:
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
                args.append([BitVector(0),BitVector(1)])
            elif isinstance(port, ArrayType):
                args.append(BitVector(x) for x in range(1<<type(port).N))
            else:
                assert True, "can't test Tuples"

    nargs = len(args)
    tests = []
    for test in product(*args):
         test = list(test)
         tests.append(test+[func(*test)])

    return tests
