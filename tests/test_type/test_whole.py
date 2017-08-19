from magma import *

def test():
    Reg2 = DefineCircuit("Reg2", "I0", In(Array2), "I1", In(Array2))
    a = Reg2.I0
    a1 = array([a[0], a[1]])
    print((a1.iswhole(a1.ts)))

    reg2 = Reg2()
    a = reg2.I0
    b = reg2.I1

    a1 = array([a[0], a[1]])
    print((a1.iswhole(a1.ts)))

    a2 = array([a[0], b[1]])
    print((a2.iswhole(a2.ts)))

    a3 = array([0,1])
    print((a3.iswhole(a3.ts)))

    a4 = a3[:1]
    print((a4.iswhole(a4.ts)))
