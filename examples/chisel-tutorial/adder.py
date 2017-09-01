
# coding: utf-8

# In[1]:


from magma import *

class FullAdder(Circuit):
    name = "FullAdder"
    IO = ["a", In(Bit), "b", In(Bit), "cin", In(Bit), "out", Out(Bit), "cout", Out(Bit)]
    @classmethod
    def definition(io):
        # Generate the sum
        _sum = io.a ^ io.b ^ io.cin
        wire(_sum, io.out)
        # Generate the carry
        carry = (io.a & io.b) | (io.b & io.cin) | (io.a & io.cin)
        wire(carry, io.cout)

def DefineAdder(N):
    T = UInt(N)
    class Adder(Circuit):
        name = "Adder{}".format(N)
        IO = ["a", In(T), "b", In(T), "cin", In(Bit), "out", Out(T), "cout", Out(Bit)]
        @classmethod
        def definition(io):
            adders = [FullAdder() for _ in range(N)]
            circ = fold(adders, foldargs={"cin":"cout"})
            wire(io.a, circ.a)
            wire(io.b, circ.b)
            wire(io.cin, circ.cin)
            wire(io.cout, circ.cout)
            wire(io.out, circ.out)
    return Adder

Adder4 = DefineAdder(4)


# In[2]:


from magma.simulator.python_simulator import testvectors

tests = testvectors(Adder4) 
print(" a  b  ci o  co")
for test in tests:
    for t in test:
        print("{:2d}".format(t), end=' ')
    print()

