from magma import *
from magma.testing import check_files_equal


@cache_definition
def DefineCoreirAdd(N, has_cout=False, has_cin=False):
    T = Bits(N)
    IO = ['in0', In(T), 'in1', In(T), 'out', Out(T)]
    gen_args = {"width": N}
    if has_cout:
        IO += ['cout', Out(Bit)]
        gen_args['has_cout'] = True
    if has_cin:
        IO += ['cin', In(Bit)]
        gen_args['has_cin'] = True
    name = "add"
    return DeclareCircuit("coreir_{}{}".format(name, N), *IO,
                      stateful=False,
                      verilog_name="coreir_" + name,
                      coreir_name=name,
                      coreir_lib = "coreir",
                      coreir_genargs=gen_args)


class DefineAdd(CircuitGenerator):
    name = "Add"
    def generate(self, n, cin=False, cout=False):
        width = n
        T = Bits(width)
        IO = ["I0", In(T), "I1", In(T)]
        if cin:
            IO += ["CIN", In(Bit)]
        IO += ["O", Out(T)]
        if cout:
            IO += ["COUT", Out(Bit)]

        circ = DefineCircuit(self.cached_name(n, cin, cout), *IO)

        add = DefineCoreirAdd(width, has_cout=cout, has_cin=cin)()
        wire(circ.I0, add.in0)
        wire(circ.I1, add.in1)
        wire(circ.O, add.out)
        if cout:
            wire(circ.COUT, add.cout)
        if cin:
            wire(circ.CIN, add.cin)
        EndDefine()
        return circ

def test_add_generator():
    compile("build/test_add8cin", DefineAdd(8, cin=True, cout=False),
            output="coreir")
    assert check_files_equal(__file__,
            "build/test_add8cin.json", "gold/test_add8cin.json")
