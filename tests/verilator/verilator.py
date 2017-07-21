from magma import BitType, ArrayType
from inspect import signature
import itertools

def harness_complete(circuit, func):
    sig = signature(func)
    nfuncargs = len(sig.parameters)

    # count inputs
    ncircargs = 0
    for name, port in circuit.interface.ports.items():
        if port.isoutput():
            ncircargs += 1
    assert nfuncargs == ncircargs

    # all arguments
    nargs = len(circuit.interface)
    ntests = 1 << (nargs-1)

    args = []
    for name, port in circuit.interface.ports.items():
        if port.isoutput():
            if isinstance(port, BitType):
                args.append([0,1])
            elif isinstance(port, ArrayType):
                args.append(range(1<<type(port).N))
            else:
                assert True, "can't test Tuples"

    tests = itertools.product(*args)

    source = '''\
#include "Vmain.h"
#include "verilated.h"
#include <cassert>
#include <iostream>

int main(int argc, char **argv, char **env) {
    Verilated::commandArgs(argc, argv);
    Vmain* top = new Vmain;
'''

    source += '''
    int tests[{}][{}] = {{
'''.format(ntests, nargs)

    for test in tests:
        testvector = ', '.join([str(test[i]) for i in range(nfuncargs)])
        testvector += ', {}'.format(func(*test[:nargs]))
        source += '''\
        {{ {} }}, 
'''.format(testvector)
    source += '''\
    };
'''

    source += '''
    for(int i = 0; i < {}; i++) {{
        int* test = tests[i];
'''.format(ntests)

    i = 0
    for name, port in circuit.interface.ports.items():
        if port.isoutput():
            source += '''\
        top->{} = test[{}];
'''.format(name,i)
        i += 1

    source += '''\
        top->eval();
'''

    i = 0
    for name, port in circuit.interface.ports.items():
        if port.isinput():
            source += '''\
        assert(top->{} == test[{}]);
    }}
'''.format(name,i)
        i += 1

    source += '''
    delete top;
    std::cout << "Success" << std::endl;
    exit(0);
}'''

    return source

def compile(filename, circuit, func):
    harness = harness_complete(circuit, func)

    with open(filename, "w") as f:
        f.write(harness)
