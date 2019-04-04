from magma import *

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
    print('inputs:', [str(p) for p in wires.inputs])
    print('outputs:', [str(p) for p in wires.outputs])
    assert len(wires.inputs) == 0
    assert len(wires.outputs) == 1
