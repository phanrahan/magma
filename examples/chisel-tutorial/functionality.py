
# coding: utf-8

# In[1]:


from magma import *


# In[2]:


def clb(a, b, c, d):
    return (a & b) | (~c & d)

T = UInt(16)
class Combinational(Circuit):
    name = "Combinational"
    IO = ["a", In(T), "b", In(T), "c", Out(T)]
    @classmethod
    def definition(io):
        wire(clb(io.a, io.b, io.a, io.b), io.c)


# In[3]:


from magma.simulator import PythonSimulator
from magma.bit_vector import BitVector

simulator = PythonSimulator(Combinational)
a = BitVector(148, num_bits=16)
b = BitVector(41, num_bits=16)
simulator.set_value(Combinational.a, a)
simulator.set_value(Combinational.b, b)
simulator.evaluate()
assert simulator.get_value(Combinational.c) == clb(a, b, a, b)
print("Success!")

