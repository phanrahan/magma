
# coding: utf-8

# In[1]:


from magma import *

class Combinational(Circuit):
    name = "Combinational"
    IO = ["x", In(UInt(16)), "y", In(UInt(16)), "z", Out(UInt(16))]
    
    @classmethod
    def definition(io):
        wire(io.x + io.y, io.z)


# In[2]:


from magma.simulator import PythonSimulator
from magma.bit_vector import BitVector

simulator = PythonSimulator(Combinational)
simulator.set_value(Combinational.x, BitVector(76, num_bits=16))
simulator.set_value(Combinational.y, BitVector(43, num_bits=16))
simulator.evaluate()
assert simulator.get_value(Combinational.z) == BitVector(76 + 43, num_bits=16)
print("Success!")

