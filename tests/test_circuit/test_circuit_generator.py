from magma import *
from magma.testing import check_files_equal


class AddGenerator(CircuitGenerator):
    base_name = "Add"
    def interface(self, N, has_cout=False, has_cin=False):
        T = Bits(N)
        IO = ['I0', In(T), 'I1', In(T), 'O', Out(T)]
        if has_cout:
            IO += ['COUT', Out(Bit)]
        if has_cin:
            IO += ['CIN', In(Bit)]
        return IO


class CoreirAdd(AddGenerator):
    @classmethod
    def definition(cls, definition, N, has_cout=False, has_cin=False):
        T = Bits(N)
        coreir_io = ['in0', In(T), 'in1', In(T), 'out', Out(T)]
        coreir_genargs = {"width": N, "has_cout": has_cout, "has_cin": has_cin}
        if has_cout:
            coreir_io += ['cout', Out(Bit)]
        if has_cin:
            coreir_io += ['cin', In(Bit)]
        CoreirAdd = DeclareCircuit("coreir_" + definition.name, *coreir_io,
                coreir_name="add", coreir_lib="coreir", coreir_genargs=coreir_genargs)
        coreir_add = CoreirAdd()
        wire(definition.I0, coreir_add.in0)
        wire(definition.I1, coreir_add.in1)
        wire(coreir_add.out, definition.O)
        if has_cout:
            wire(coreir_add.cout, definition.COUT)
        if has_cin:
            wire(coreir_add.cin, definition.CIN)


def test_add_generator():
    Add8cin = AddGenerator(8, has_cin=True, has_cout=False)
    assert Add8cin._generator_arguments.args == (8,)
    assert Add8cin._generator_arguments.kwargs == {"has_cin": True, "has_cout": False}
    assert Add8cin._generator == AddGenerator
    test_circuit = DefineCircuit("test", "I0", In(Bits(8)), "I1", In(Bits(8)),
            "CIN", In(Bit), "O", Out(Bits(8)))
    adder = Add8cin()
    wire(test_circuit, adder)
    wire(test_circuit.O, adder.O)
    EndDefine()
    compile("build/test_add8cin", test_circuit, output="coreir",
            generators=[CoreirAdd])
    assert check_files_equal(__file__,
            "build/test_add8cin.json", "gold/test_add8cin.json")
