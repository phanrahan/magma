from magma import *
from magma.testing import check_files_equal


def test():
    class And2(Circuit):
        name = "And2"
        io = IO(I0=In(Bit), I1=In(Bit), O=Out(Bit))

    class main(Circuit):
        name = "main"
        io = IO(I0=In(Bit), I1=In(Bit), O=Out(Bit))
        I = array([io.I0, io.I1])
        O = io.O

        class AndN2:
            def __init__(self):
                and2 = And2()
                self.I = array([and2.I0, and2.I1])
                self.O = and2.O

            def __call__(self, I):
                wire(I, self.I)
                return self.O

        and2 = AndN2()

        O( and2(I) )

    compile("build/class", main, output="verilog")
    assert check_files_equal(__file__, "build/class.v", "gold/class.v")
