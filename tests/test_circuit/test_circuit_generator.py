from magma import *
from magma.testing import check_files_equal
from collections import namedtuple


@circuit_generator
def DefineAdd(N, has_cout=False, has_cin=False):
    T = Bits(N)
    IO_ = ['I0', In(T), 'I1', In(T), 'O', Out(T)]
    name_ = "Add{}".format(N)
    if has_cout:
        IO_ += ['COUT', Out(Bit)]
        name_ += "_cout"
    if has_cin:
        IO_ += ['CIN', In(Bit)]
        name_ += "_cin"
    class Add(Circuit):
        # Underscores because there's some weird scoping issue here with Python
        # when trying to capture name and IO
        name = name_
        IO = IO_
    return Add

# Mock importing DefineAdd from external module using a namedtuple
primitives = namedtuple('primitives', ['DefineAdd'])(DefineAdd)


@circuit_generator
def DefineAdd(N, has_cout=False, has_cin=False):
    class Add(primitives.DefineAdd(N, has_cout, has_cin)):
        @classmethod
        def definition(add):
            T = Bits(N)
            coreir_io = ['in0', In(T), 'in1', In(T), 'out', Out(T)]
            coreir_genargs = {"width": N, "has_cout": has_cout, "has_cin": has_cin}
            if has_cout:
                coreir_io += ['cout', Out(Bit)]
            if has_cin:
                coreir_io += ['cin', In(Bit)]
            CoreirAdd = DeclareCircuit("coreir_" + add.name, *coreir_io,
                    coreir_name="add", coreir_lib="coreir",
                    coreir_genargs=coreir_genargs)
            coreir_add = CoreirAdd()
            wire(add.I0, coreir_add.in0)
            wire(add.I1, coreir_add.in1)
            wire(coreir_add.out, add.O)
            if has_cout:
                wire(coreir_add.cout, add.COUT)
            if has_cin:
                wire(coreir_add.cin, add.CIN)
    return Add


def test_add_generator():
    Add8cin = DefineAdd(8, has_cin=True, has_cout=False)
    assert Add8cin._generator_arguments.args == (8,)
    assert Add8cin._generator_arguments.kwargs == {"has_cin": True, "has_cout": False}
    test_circuit = DefineCircuit("test", "I0", In(Bits(8)), "I1", In(Bits(8)),
            "CIN", In(Bit), "O", Out(Bits(8)))
    adder = Add8cin()
    wire(test_circuit, adder)
    wire(test_circuit.O, adder.O)
    EndDefine()
    print(repr(test_circuit))
    compile("build/test_add8cin", test_circuit, output="coreir")
    assert check_files_equal(__file__,
            "build/test_add8cin.json", "gold/test_add8cin.json")
