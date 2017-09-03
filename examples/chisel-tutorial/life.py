
# coding: utf-8

# In[1]:


from magma import *
from magma.primitives import DefineRegister
from functools import reduce

def and_(in0, in1):
    if isinstance(in0, list) and isinstance(in1, list):
        return [and_(x, y) for x, y in zip(in0, in1)]
    else:
        return in0 & in1

def or_(in0, in1):
    if isinstance(in0, list) and isinstance(in1, list):
        return [and_(x, y) for x, y in zip(in0, in1)]
    else:
        return in0 | in1

def one_hot_mux(conds, inputs):
    outputs = []
    for cond, inp in zip(conds, inputs):
        if isinstance(inp, BitType):
            outputs.append(inp & cond)
        else:
            outputs.append(and_(inp, [cond for _ in range(len(inp))]))
    return reduce(lambda x, y: or_(x, y), outputs)


def mux(conds, inputs):
    return one_hot_mux(conds, inputs)


def count_neighbors(neighbors):
    return reduce(lambda x, y: uint(y, 3) + x, neighbors, uint(0, 3))


Register1 = DefineRegister(1)

class Cell(Circuit):
    name = "Cell"
    IO = ["neighbors", In(Array(8, UInt(1))), "out", Out(Bit), 
          "running", In(Bit), "write_enable", In(Bit), 
          "write_value", In(Bit), "CLK", In(Bit)]
    
    @classmethod
    def definition(io):
        is_alive = Register1()
        wire(io.CLK, is_alive.clk)
        
        not_running_out = mux([io.write_enable, ~io.write_enable], [io.write_value, is_alive.Q[0]])
        
        count = count_neighbors(io.neighbors)
        alive_out = mux([count < int2seq(2, 3), 
                         int2seq(2, 3) <= count < int2seq(4, 3), 
                         count >= int2seq(4, 3)],
                        [[False], [True], [False]])
        
        not_alive_cond = and_(~is_alive.Q[0], count == int2seq(3, 3))
        not_alive_out = mux([not_alive_cond, ~not_alive_cond], [[True], [False]])
        
        running_out = mux([is_alive.Q[0]], [alive_out, not_alive_out])
        out = mux([io.running, ~io.running], [running_out[0], not_running_out])
        wire(out, is_alive.D[0])
        wire(out, io.out)
        
n = 4

def index(i, j):
    return ((j + n) % n) * n + ((i + n) % n)

total = n * n

class Life(Circuit):
    name = "Life"
    IO = ["state", Out(Array(total, Bit)),
          "running", In(Bit),
          "write_value", In(Bit),
          "write_address", In(UInt(log2(n + 1))),
          "CLK", In(Bit)]
    
    @classmethod
    def definition(io):
        cells = [Cell() for _ in range(total)]
        for k in range(0, total):
            wire(io.CLK, cells[k].CLK)
            wire(cells[k].out, io.state[k])
            wire(cells[k].running, io.running)
            wire(cells[k].write_value, io.write_value)
            wire(cells[k].write_enable, io.write_address == int2seq(k, log2(n+1)))
        
        for j in range(0, n):
            for i in range(0, n):
                cell = cells[j * n + 1]
                ni = 0
                for dj in range(-1, 1):
                    for di in range(-1, 1):
                        if (di != 0 or dj != 0):
                            wire(cells[index(i + di, j + dj)].out, cell.neighbors[ni][0])
                            ni = ni + 1
    


# In[2]:


from magma.python_simulator import PythonSimulator
from magma.scope import Scope
from magma.bit_vector import BitVector

simulator = PythonSimulator(Life)
scope = Scope()


# In[ ]:




