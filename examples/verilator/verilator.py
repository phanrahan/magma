from function import testvectors

__all__ = ['harness', 'compile']

def harness(circuit,tests):

    assert len(circuit.interface.ports.keys()) == len(tests[0])

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
        testvector = ', '.join([str(int(t)) for t in test])
        #testvector += ', {}'.format(int(func(*test[:nargs])))
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

def compile(filename, circuit, tests):
    if callable(tests):
        tests = testvectors(circuit, tests)
    verilatorcpp = harness(circuit, tests)

    with open(filename, "w") as f:
        f.write(verilatorcpp)
