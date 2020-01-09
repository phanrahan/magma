from magma import *
from magma.testing import check_files_equal

# test anonymous bits

def test():
    b0 = Bit(name='b0')
    assert b0.direction is None

    b1 = Bit()
    assert b1.direction is None

    print('wire(b0,b1)')
    wire(b0,b1)
    assert b0.port.wires is b1.port.wires

    wires = b0.port.wires
    assert len(wires.inputs) == 0
    assert len(wires.outputs) == 1
    print('inputs:', [str(p) for p in wires.inputs])
    print('outputs:', [str(p) for p in wires.outputs])


def test_anon_bits():
    class Test(Circuit):
        IO = ["I", In(Bits[5]), "O", Out(Bits[5])]

        @classmethod
        def definition(io):
            x = Bits[5]()
            y = Bits[5]()
            y @= io.I
            x @= y
            io.O @= x
    compile("build/test_anon_bits", Test, output="coreir-verilog")
    assert check_files_equal(__file__, f"build/test_anon_bits.v",
                             f"gold/test_anon_bits.v")
