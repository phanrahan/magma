from .test_primitives import *
from magma.simulator import PythonSimulator
from magma import *
from magma.scope import *

def test():
    def FFs(n):
        return [PRIM_FF() for i in range(n)]
    
    def Register(n):
        args = ["I", In(Array(n, Bit)), "O", Out(Array(n, Bit))] + ClockInterface(False, False, False)
    
        RegCircuit = DefineCircuit('Register' + str(n), *args)
        ffs = join(FFs(n))
        wire(RegCircuit.I, ffs.D)
        wire(ffs.Q, RegCircuit.O)
        EndCircuit()
    
        return RegCircuit()
    
    def IncOne(n):
        def sim_inc_one(self, value_store, state_store):
            I = value_store.get_value(self.I)
            n = len(I)
            val = seq2int(I) + 1
    
            cout = val > ((1 << n) - 1)
            val = val % (1 << n)
    
            seq = int2seq(val, len(I))
            seq = [bool(s) for s in seq]
            value_store.set_value(self.O, seq)
            value_store.set_value(self.COUT, cout)
    
        args = ["I", In(Array(n, Bit)), "O", Out(Array(n, Bit)), "COUT", Out(Bit)]
        return DeclareCircuit('IncOne' + str(n), *args, stateful=False, primitive=True, simulate=sim_inc_one)()
    
    def TestCounter(n):
        args = []
    
        args += ["O", Array(n, Out(Bit))]
        args += ["COUT", Out(Bit)]
    
        args += ClockInterface(False, False, False)
    
        Counter = DefineCircuit('Counter' + str(n), *args)
    
        inc = IncOne(n)
        reg = Register(n)
    
        wire(reg.O, inc.I)
        wire(inc.O, reg.I)
        wire(reg.O, Counter.O)
    
        wire(inc.COUT, Counter.COUT)
    
        wireclock(Counter, reg)
    
        EndCircuit()
    
        return Counter()
    
    args = ['O', Array(5, Out(Bit)), 'COUT', Out(Bit)]
    args += ClockInterface(False, False, False)
    
    testcircuit = DefineCircuit('Test', *args)
    counter = TestCounter(5)
    wire(counter.O, testcircuit.O)
    wire(counter.COUT, testcircuit.COUT)
    EndCircuit()
    
    sim = PythonSimulator(testcircuit, testcircuit.CLK)
    
    for i in range((1 << 5) - 1):
        sim.advance()
        val = sim.get_value(testcircuit.O)
        num = seq2int(val)
        assert num == i
        cout = sim.get_value(testcircuit.COUT)
        assert not cout
    
        sim.advance()
    
    val = sim.get_value(testcircuit.O)
    num = seq2int(val)
    assert num == 31
    cout = sim.get_value(testcircuit.COUT)
    assert cout
    

    sim.advance()
    sim.advance()
    
    val = sim.get_value(testcircuit.O)
    num = seq2int(val)
    assert num == 0
    
    cout = sim.get_value(testcircuit.COUT)
    assert not cout
