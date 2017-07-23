from magma import BitType, ArrayType
from inspect import signature
import itertools

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

def generate_tests(circuit, func):
    args = []
    for name, port in circuit.interface.ports.items():
        if port.isoutput():
            if isinstance(port, BitType):
                args.append([0,1])
            elif isinstance(port, ArrayType):
                args.append(range(1<<type(port).N))
            else:
                assert True, "can't test Tuples"

    nargs = len(args)
    tests = []
    for test in itertools.product(*args):
         test = list(test)
         tests.append(test+[func(*test)])

    return tests

def harness(circuit,tests):

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
'''.format(len(tests), len(tests[0]))

    for test in tests:
        testvector = ', '.join([str(t) for t in test])
        #testvector += ', {}'.format(func(*test[:nargs]))
        source += '''\
        {{ {} }}, 
'''.format(testvector)
    source += '''\
    };
'''

    source += '''
    for(int i = 0; i < {}; i++) {{
        int* test = tests[i];
'''.format(len(tests))

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

def harness_complete(circuit, func):
    check(circuit, func)
    tests = generate_tests(circuit, func)
    return harness(circuit, tests)


def compile(filename, circuit, func):
    harness = harness_complete(circuit, func)

    with open(filename, "w") as f:
        f.write(harness)
