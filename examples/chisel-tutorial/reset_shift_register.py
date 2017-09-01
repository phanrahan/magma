
# coding: utf-8

# In[1]:


from magma import *
from magma.primitives import DefineRegister

N = 4
Register4 = DefineRegister(4, has_reset=True)
T = Bits(N)

class ResetShiftRegister(Circuit):
    name = "ResetShiftRegister"
    IO = ["I", In(T), "reset", In(Bit), "O", Out(T)] + ClockInterface()
    @classmethod
    def definition(io):
        regs = [Register4().reset(io.reset) for _ in range(4)]
        wireclock(io, regs)
        wire(io.I, getattr(regs[0], "in"))
        fold(regs, foldargs={"in":"out"})
        wire(regs[-1].out, io.O)


# In[2]:


from magma.backend.verilog import compile as compile_verilog
print(compile_verilog(ResetShiftRegister))


# In[3]:


from magma.simulator import PythonSimulator
from magma.bit_vector import BitVector

simulator = PythonSimulator(ResetShiftRegister, clock=ResetShiftRegister.CLK)
outputs = []
simulator.set_value(ResetShiftRegister.reset, True)
for i in range(0, 1 << N):
    simulator.set_value(ResetShiftRegister.I, BitVector(i, N))
    
    for j in range(2):
        if i == 9:
            if j == 0:
                simulator.set_value(ResetShiftRegister.reset, False)
            else:
                simulator.set_value(ResetShiftRegister.reset, True)
        simulator.step()
        simulator.evaluate()
        O = simulator.get_value(ResetShiftRegister.O)
        outputs.append(BitVector(O).as_int())

print(outputs)

