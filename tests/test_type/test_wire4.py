from magma import *

def test():
    b0 = BitIn(name='b0')
    b1 = BitIn(name='b1')

    print('wire(b0,b1)')
    wire(b0,b1)
    #assert b0.port.wires is b1.port.wires

    #wires = b0.port.wires
    #print 'inputs:', [str(p) for p in wires.inputs]
    #print 'outputs:', [str(p) for p in wires.outputs]

    assert len(b0.port.wires.inputs) == 0
    assert len(b0.port.wires.outputs) == 0

    assert not b0.wired()
    assert not b1.wired()

    assert b0.trace() is None
    assert b1.trace() is None

    assert b0.value() is None
    assert b1.value() is None
