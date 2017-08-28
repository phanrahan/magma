from magma import BitType, ArrayType, SIntType
from magma.bit_vector import BitVector
import sys
if sys.version_info < (3, 3):
    from funcsigs import signature
else:
    from inspect import signature
from itertools import product
import pytest

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

@pytest.mark.skip(reason="Not a test")
def testvectors(circuit, func, input_ranges=None, mode='complete'):
    check(circuit, func)

    args = []
    for i, (name, port) in enumerate(circuit.interface.ports.items()):
        if port.isoutput():
            if isinstance(port, BitType):
                args.append([BitVector(0),BitVector(1)])
            elif isinstance(port, ArrayType):
                num_bits = type(port).N
                if isinstance(port, SIntType):
                    if input_ranges is None:
                        start = -2**(num_bits - 1)
                        end = 2**(num_bits - 1)  # We don't subtract one because range end is exclusive
                        input_range = range(start, end)
                    else:
                        input_range = input_ranges[i]
                    args.append([BitVector(x, num_bits=num_bits, signed=True) for x in input_range])
                else:
                    if input_ranges is None:
                        input_range = range(1<<num_bits)
                    else:
                        input_range = input_ranges[i]
                    args.append([BitVector(x, num_bits=num_bits) for x in input_range])
            else:
                assert True, "can't test Tuples"

    nargs = len(args)
    tests = []
    for test in product(*args):
        test = list(test)
        result = func(*test)
        if isinstance(result, tuple):
            test.extend(result)
        else:
            test.append(result)
        tests.append(test)

    return tests
