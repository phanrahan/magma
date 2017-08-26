from magma import *

def test():
    Tuple2 = Tuple(x=Bit, y=Bit)

    t0 = Tuple2(name='t0')
    #assert t0.direction is None

    t1 = Tuple2(name='t1')
    #assert t1.direction is None

    wire(t0, t1)

    assert t0.wired()
    assert t1.wired()

    assert t1.driven()

    assert t0.trace() is t1
    assert t1.trace() is t0

    #print t0.driven()
    assert t0.value() is None
    assert t1.value() is t0

    b0 = t0.x
    b1 = t1.x

    assert b0.port.wires is b1.port.wires

    wires = b0.port.wires
    assert len(b0.port.wires.inputs) == 1
    assert len(b0.port.wires.outputs) == 1
    print('inputs:', [str(p) for p in wires.inputs])
    print('outputs:', [str(p) for p in wires.outputs])


