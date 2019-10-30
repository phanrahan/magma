from magma import *
from magma.testing import check_files_equal


def test():
    DFF = DeclareCircuit('DFF', "I", In(Bit), "O", Out(Bit), "CLK", In(Clock))

    def FFs(n):
        return [DFF() for i in range(n)]

    main = DefineCircuit("main", "CLK", In(Clock), "I", In(Bits[2]), "O", Out(Bits[2]))
    I = main.I
    O = main.O

    def Register(n, ce=False, r=False, s=False):

         T = Array[n, Bit]
         class RegisterCircuit(Circuit):
              name = 'Register' + str(n)
              IO = ["I", In(T), "O", Out(T)] + ClockInterface(ce,r,s)
              @classmethod
              def definition(reg):
                  print('join')
                  ffs = join(FFs(n))

                  print('reg.I')
                  wire(reg.I, ffs.I)
                  print('reg.O')
                  wire(ffs.O, reg.O)

         return RegisterCircuit

    Register2 = Register(2)
    #print(Register2, Register2.IO)

    reg = Register2()

    print('wire I')
    wire(I, reg.I)
    print('wire O')
    wire(reg.O, O)

    compile("build/creg", main, output="verilog")
    assert check_files_equal(__file__, "build/creg.v", "gold/creg.v")

