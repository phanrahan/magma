
# coding: utf-8

# In[1]:


import magma as m
from magma.primitives import DefineRegister

N = 4
Register4 = DefineRegister(4)
T = m.Bits(N)

class ShiftRegister(m.Circuit):
    name = "ShiftRegister"
    IO = ["I", m.In(T), "O", m.Out(T)] + m.ClockInterface()
    @classmethod
    def definition(io):
        regs = [Register4() for _ in range(N)]
        m.wireclock(io, regs)
        m.wire(io.I, getattr(regs[0], "in"))
        m.fold(regs, foldargs={"in":"out"})
        m.wire(regs[-1].out, io.O)


# In[2]:


from magma.backend.verilog import compile as compile_verilog
print(compile_verilog(ShiftRegister))


# In[3]:


from magma.simulator import PythonSimulator
from magma.bit_vector import BitVector

simulator = PythonSimulator(ShiftRegister, clock=ShiftRegister.CLK)
outputs = []
for i in range(0, 1 << N):
    simulator.set_value(ShiftRegister.I, BitVector(i, N))
    for j in range(2):
        simulator.step()
        simulator.evaluate()
        O = simulator.get_value(ShiftRegister.O)
        outputs.append(BitVector(O))

print([val.as_int() for val in outputs])

