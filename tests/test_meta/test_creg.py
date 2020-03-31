from magma import *
from magma.testing import check_files_equal


def test():
    class DFF(Circuit):
        name = "DFF"
        io = IO(I=In(Bit), O=Out(Bit), CLK=In(Clock))

    def FFs(n):
        return [DFF() for i in range(n)]

    class main(Circuit):
        name = "main"
        io = IO(CLK=In(Clock), I=In(Bits[2]), O=Out(Bits[2]))
        I = io.I
        O = io.O

        def Register(n, ce=False, r=False, s=False):

            T = Array[n, Bit]

            class RegisterCircuit(Circuit):
                name = "Register" + str(n)
                io = IO(I=In(T), O=Out(T)) + ClockIO(ce, r, s)
                print("join")
                ffs = join(FFs(n))

                print("io.I")
                wire(io.I, ffs.I)
                print("io.O")
                wire(ffs.O, io.O)

            return RegisterCircuit

        Register2 = Register(2)
        #print(Register2, Register2.IO)

        reg = Register2()

        print("wire I")
        wire(I, reg.I)
        print("wire O")
        wire(reg.O, O)

    compile("build/creg", main, output="verilog")
    assert check_files_equal(__file__, "build/creg.v", "gold/creg.v")
