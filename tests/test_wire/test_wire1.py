from magma import *

def test():
    b0 = BitOut(name='b0')
    assert b0.isoutput()

    b1 = BitIn(name='b1')
    assert b1.isinput()

    print('wire(b0,b1)')
    wire(b0,b1)
    assert b0.port.wires is b1.port.wires

    #wires = b0.port.wires
    #print 'inputs:', [str(p) for p in wires.inputs]
    #print 'outputs:', [str(p) for p in wires.outputs]
    assert len(b0.port.wires.inputs) == 1
    assert len(b0.port.wires.outputs) == 1

    assert b0.wired()
    assert b1.wired()

    assert b0.trace() is b1
    assert b1.trace() is b0

    assert b0.value() is None
    assert b1.value() is b0
