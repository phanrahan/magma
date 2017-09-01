
# coding: utf-8

# In[1]:


import sys
sys.path.append("../../examples")
from full_adder import FullAdder
from magma import *


# In[2]:


T = Bits(4)
class Adder4(Circuit):
    name = "Adder4"
    IO = ["a", In(T), "b", In(T), "cin", In(Bit), "out", Out(T), "cout", Out(Bit)]
    @classmethod
    def definition(io):
        adder1 = FullAdder()
        wire(io.a[0], adder1.a)
        wire(io.b[0], adder1.b)
        wire(io.cin, adder1.cin)
        adder2 = FullAdder()
        wire(io.a[1], adder2.a)
        wire(io.b[1], adder2.b)
        wire(adder1.cout, adder2.cin)
        adder3 = FullAdder()
        wire(io.a[2], adder3.a)
        wire(io.b[2], adder3.b)
        wire(adder2.cout, adder3.cin)
        adder4 = FullAdder()
        wire(io.a[3], adder4.a)
        wire(io.b[3], adder4.b)
        wire(adder3.cout, adder4.cin)
        
        wire(adder4.cout, io.cout)
        wire(bits([adder1.out, adder2.out, adder3.out, adder4.out]), io.out)


# In[3]:


from magma.simulator import PythonSimulator
from magma.bit_vector import BitVector

simulator = PythonSimulator(Adder4)
simulator.set_value(Adder4.a, BitVector(2, num_bits=4))
simulator.set_value(Adder4.b, BitVector(3, num_bits=4))
simulator.set_value(Adder4.cin, True)
simulator.evaluate()
assert simulator.get_value(Adder4.out) == BitVector(6, num_bits=4)
assert simulator.get_value(Adder4.cout) == False
print("Success!")

