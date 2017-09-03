
# coding: utf-8

# In[1]:


from magma import *
from functools import reduce

def one_hot_mux(conds, inputs):
    outputs = []
    for cond, inp in zip(conds, inputs):
        outputs.append(inp & uint([cond for _ in range(len(inp))]))
    return reduce(lambda x, y: x | y, outputs)


class SimpleALU(Circuit):
    name = "SimpleALU"
    IO = ["a", In(UInt(4)), "b", In(UInt(4)), "opcode", In(UInt(2)), "out", Out(UInt(4))]
    
    @classmethod
    def definition(io):
        is_op0 = io.opcode == uint(0, n=2)
        is_op1 = io.opcode == uint(1, n=2)
        is_op2 = io.opcode == uint(2, n=2)
        is_op3 = io.opcode == uint(3, n=2)
        op0_out = io.a + io.b
        op1_out = io.a - io.b
        op2_out = io.a
        op3_out = io.b
        wire(io.out, one_hot_mux([is_op0, is_op1, is_op2, is_op3], [op0_out, op1_out, op2_out, op3_out]))


# In[2]:


from magma.backend.verilog import compile as compile_verilog

print(compile_verilog(SimpleALU))


# In[3]:


from magma.simulator import PythonSimulator
from magma.bit_vector import BitVector

simulator = PythonSimulator(SimpleALU)
simulator.set_value(SimpleALU.a, BitVector(3, num_bits=4))
simulator.set_value(SimpleALU.b, BitVector(2, num_bits=4))
simulator.set_value(SimpleALU.opcode, BitVector(0, num_bits=2))
simulator.evaluate()
assert simulator.get_value(SimpleALU.out) == BitVector(3 + 2, num_bits=4)

simulator.set_value(SimpleALU.a, BitVector(3, num_bits=4))
simulator.set_value(SimpleALU.b, BitVector(2, num_bits=4))
simulator.set_value(SimpleALU.opcode, BitVector(1, num_bits=2))
simulator.evaluate()
assert simulator.get_value(SimpleALU.out) == BitVector(3 - 2, num_bits=4)

simulator.set_value(SimpleALU.a, BitVector(3, num_bits=4))
simulator.set_value(SimpleALU.b, BitVector(2, num_bits=4))
simulator.set_value(SimpleALU.opcode, BitVector(2, num_bits=2))
simulator.evaluate()
assert simulator.get_value(SimpleALU.out) == BitVector(3, num_bits=4)

simulator.set_value(SimpleALU.a, BitVector(3, num_bits=4))
simulator.set_value(SimpleALU.b, BitVector(2, num_bits=4))
simulator.set_value(SimpleALU.opcode, BitVector(3, num_bits=2))
simulator.evaluate()
assert simulator.get_value(SimpleALU.out) == BitVector(2, num_bits=4)
print("Success!")

