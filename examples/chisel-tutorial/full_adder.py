
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


# In[2]:


from magma.backend.verilog import compile as compile_verilog

print(compile_verilog(FullAdder))


# In[3]:


from magma.simulator.python_simulator import testvectors

test_vectors = [
    [0, 0, 0, 0, 0],
    [0, 0, 1, 1, 0],
    [0, 1, 0, 1, 0],
    [0, 1, 1, 0, 1],
    [1, 0, 0, 1, 0],
    [1, 0, 1, 0, 1],
    [1, 1, 0, 0, 1],
    [1, 1, 1, 1, 1]
]

tests = testvectors(FullAdder)
print(tests)
print( "Success" if tests == test_vectors else "Failure" )


# In[4]:


from magma.waveform import waveform

waveform(tests, ["a", "b", "cin", "sum", "cout"])

