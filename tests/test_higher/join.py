from magma import *

def test():
    And2 = DeclareCircuit('And2', "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))

    and0 = And2(name='and0')
    and1 = And2(name='and1')

    a = join(and0, and1)
    print(repr(a))

test()
