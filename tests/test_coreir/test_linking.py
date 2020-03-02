import os
import magma as m
from magma.frontend.coreir_ import coreir_typegen, DeclareCoreIRGenerator
from magma.testing import check_files_equal

# def smax_type_gen(context, values):
#     width = values['width'].value
#     return context.Record({
#         "in0": context.Array(width, context.BitIn()),
#         "in1": context.Array(width, context.BitIn()),
#         "out": context.Array(width, context.Bit())
#     })


@coreir_typegen
def smax_type_gen(width: int):
    class T(m.Product):
        in0 = m.Array[width, m.In(m.Bit)]
        in1 = m.Array[width, m.In(m.BitIn)]
        out = m.Array[width, m.In(m.Bit)]
    return T


def test_declare_generator():
    DefineSmax = DeclareCoreIRGenerator(lib="commonlib", name="smax")
    width = 16

    class LinkerTest(m.Circuit):
        name = "LinkerTest0"
        io = m.IO(I0=m.In(m.Bits[width]), I1=m.In(m.Bits[width]),
                  O=m.Out(m.Bits[width]))

        Smax = DefineSmax(width=width)
        smax = Smax()
        m.wire(io.I0, smax.in0)
        m.wire(io.I1, smax.in1)
        m.wire(io.O, smax.out)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    m.compile(os.path.join(dir_path, "build/linker_test0"), LinkerTest,
              output="coreir")

    assert check_files_equal(__file__, "build/linker_test0.json",
                             "gold/linker_test0.json")
