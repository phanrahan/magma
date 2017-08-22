from magma import *

def test():
    And2 = DeclareCircuit('And2', "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))
    and1 = And2(name='and1')
    and2 = uncurry(and1)
    and3 = curry(and2)
    print(repr(and1))
    print(repr(and2))
    print(repr(and3))
    
test()
