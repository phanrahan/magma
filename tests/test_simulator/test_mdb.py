from .test_primitives import *
from magma.simulator import PythonSimulator
from magma.simulator.mdb import SimulationConsole
from magma import *
from magma.scope import *
from magma.passes.debug_name import DebugNamePass

def test(capsys):
    def get_out(capsys):
        out, err = capsys.readouterr()
        assert(err == "")
        return out.rstrip()

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

    DebugNamePass(testcircuit).run()

    console = SimulationConsole(testcircuit, sim);
    sim.evaluate()

    console.runcmd("p self.O")
    out, err = capsys.readouterr()
    assert(out.rstrip() == "0")

    console.runcmd("p self.idontexist")
    out, err = capsys.readouterr()
    assert(err != "")
    assert(out == "")

    console.runcmd("next")
    console.runcmd("next")
    out, err = capsys.readouterr()
    assert(err == "")
    assert(out == "")

    console.runcmd("p self.O")
    assert get_out(capsys) == "1"

    console.runcmd("next")
    console.runcmd("p self.O")
    assert get_out(capsys) == "2"

    console.runcmd("p counter.O")
    assert get_out(capsys) == "2"

    console.runcmd("p counter.reg.O")
    assert get_out(capsys) == "2"
