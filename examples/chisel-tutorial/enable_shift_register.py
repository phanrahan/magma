
# coding: utf-8

# In[1]:


from magma import *
from magma.primitives import DefineRegister

N = 4
Register4 = DefineRegister(4, has_ce=True)
T = Bits(N)

class EnableShiftRegister(Circuit):
    name = "EnableShiftRegister"
    IO = ["I", In(T), "shift", In(Bit), "O", Out(T)] + ClockInterface()
    @classmethod
    def definition(io):
        regs = [Register4().when(io.shift) for _ in range(N)]
        wireclock(io, regs)
        wire(io.I, getattr(regs[0], "in"))
        fold(regs, foldargs={"in":"out"})
        wire(regs[-1].out, io.O)


# In[2]:


from magma.backend.verilog import compile as compile_verilog
print(compile_verilog(EnableShiftRegister))


# In[3]:


from magma.simulator import PythonSimulator
from magma.bit_vector import BitVector

simulator = PythonSimulator(EnableShiftRegister, clock=EnableShiftRegister.CLK)
outputs = []
for i in range(1 << N):
    simulator.set_value(EnableShiftRegister.I, BitVector(i, N))
    simulator.set_value(EnableShiftRegister.shift, bool(i % 2))
    for j in range(2):
        simulator.step()
        simulator.evaluate()
        O = simulator.get_value(EnableShiftRegister.O)
        outputs.append(BitVector(O).as_int())
        
print(outputs)

