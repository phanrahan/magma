import sys
from magma import *


def test():
    And2 = DeclareCircuit('And2', "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))

    main = DefineCircuit("main", "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))
    I = array(main.I0, main.I1) 
    O = main.O

    class AndN2:
        def __init__(self):
            and2 = And2()
            self.I = array(and2.I0, and2.I1)
            self.O = and2.O

        def __call__(self, I):
            wire(I, self.I)
            return self.O

    and2 = AndN2()

    O( and2(I) )

    compile("build/class", main)
    assert magma_check_files_equal(__file__, "build/class.v", "gold/class.v")
