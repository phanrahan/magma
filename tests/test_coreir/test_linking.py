import os
import magma as m
import coreir

# def smax_type_gen(context, values):
#     width = values['width'].value
#     return context.Record({
#         "in0": context.Array(width, context.BitIn()),
#         "in1": context.Array(width, context.BitIn()),
#         "out": context.Array(width, context.Bit())
#     })

@m.coreir_typegen
def smax_type_gen(width : int):
    return Tuple(
        in0 = m.Array(width, m.In(m.Bit)),
        in1 = m.Array(width, m.In(m.BitIn)),
        out = m.Array(width, m.In(m.Bit))
    )


def test_declare_generator():
    DefineSmax = m.DeclareCoreIRGenerator(lib="commonlib", name="smax", typegen=smax_type_gen)
    width = 16

    class LinkerTest(m.Circuit):
        name = "LinkerTest0"
        IO = ["I0", m.In(m.Bits(width)), "I1", m.In(m.Bits(width)), "O", m.Out(m.Bits(width))]
        @classmethod
        def definition(self):
            Smax = DefineSmax(width=width)
            smax = Smax()
            m.wire(self.I0, smax.in0)
            m.wire(self.I1, smax.in1)
            m.wire(self.O, smax.out)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    m.compile(os.path.join(dir_path, "build/linker_test0"), LinkerTest, output="coreir")
    with open(os.path.join(dir_path, "build/linker_test0.json"), "r") as actual:
        with open(os.path.join(dir_path, "gold/linker_test0.json"), "r") as expected:
            assert actual.read() == expected.read()
