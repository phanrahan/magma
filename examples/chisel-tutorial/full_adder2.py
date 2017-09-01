
# coding: utf-8

# In[1]:


from magma import *

class FullAdder(Circuit):
    name = "FullAdder"
    IO = ["a", In(Bit), "b", In(Bit), "cin", In(Bit), "out", Out(Bit), "cout", Out(Bit)]
    @classmethod
    def definition(io):
        # Generate the sum
        sum_ = xor(io.a, io.b, io.cin)
        wire(sum_, io.out)
        # Generate the carry
        ab = and_(io.a, io.b)
        bc = and_(io.b, io.cin)
        ca = and_(io.cin, io.a)
        carry = or_(ab, bc, ca)
        wire(carry, io.cout)


# In[2]:


from magma.backend.verilog import compile as compile_verilog

#print(repr(FullAdder))
print(compile_verilog(FullAdder))


# In[4]:


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


# In[5]:


from magma.waveform import waveform

waveform(tests, ["a", "b", "cin", "sum", "cout"])


# In[ ]:




