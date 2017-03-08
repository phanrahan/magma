from magma import *

def test():
    a0 = Array2(name='a0')
    #assert a0.direction is None

    a1 = Array2(name='a1')
    #assert a1.direction is None

    wire(a0, a1)

    assert a0.wired()
    assert a1.wired()

    assert a1.driven()

    assert a0.trace() is a1
    assert a1.trace() is a0

    #print a0.driven()
    assert a0.value() is None
    assert a1.value() is a0

    b0 = a0[0]
    b1 = a1[0]

    assert b0.port.wires is b1.port.wires

    wires = b0.port.wires
    assert len(b0.port.wires.inputs) == 1
    assert len(b0.port.wires.outputs) == 1
    print('inputs:', [str(p) for p in wires.inputs])
    print('outputs:', [str(p) for p in wires.outputs])
