from .test_primitives import *
import magma as m
from magma.simulator import PythonSimulator
from magma.simulator.mdb import SimulationConsole
from magma import *
from magma.scope import *
from magma.passes.debug_name import DebugNamePass
from magma.passes.clock import drive_undriven_other_clock_types_in_inst

def test(capsys):
    m.config.set_debug_mode(True)
    def get_out(capsys):
        out, err = capsys.readouterr()
        assert(err == "")
        return out.rstrip()

    def FFs(n):
        return [PRIM_FF() for i in range(n)]
    
    def Register(n):
        args = ["I", In(Array[n, Bit]), "O", Out(Array[n, Bit])] + ClockInterface(False, False, False)

        class RegCircuit(m.Circuit):
            name = 'Register' + str(n)
            io = m.IO(**dict(zip(args[::2], args[1::2])))
            ffs = join(FFs(n))
            wire(io.I, ffs.D)
            wire(ffs.Q, io.O)
    
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
    
        args = ["I", In(Array[n, Bit]), "O", Out(Array[n, Bit]), "COUT", Out(Bit)]
        class _Circuit(Circuit):
            name = 'IncOne' + str(n)
            io = IO(**dict(zip(args[::2], args[1::2])))
            stateful = False
            primitive = True
            simulate = sim_inc_one

        return _Circuit()
    
    def TestCounter(n):
        args = []
    
        args += ["O", Array[n, Out(Bit)]]
        args += ["COUT", Out(Bit)]
    
        args += ClockInterface(False, False, False)
    
        class Counter(m.Circuit):
            name = 'Counter' + str(n)
            io = m.IO(**dict(zip(args[::2], args[1::2])))
    
            inc = IncOne(n)
            reg = Register(n)
            reg.name = "reg"
    
            wire(reg.O, inc.I)
            wire(inc.O, reg.I)
            wire(reg.O, io.O)
    
            wire(inc.COUT, io.COUT)
    
        drive_undriven_other_clock_types_in_inst(Counter, Counter.reg)
    
        return Counter()
    
    args = ['O', Array[5, Out(Bit)], 'COUT', Out(Bit)]
    args += ClockInterface(False, False, False)
    
    class testcircuit(Circuit):
        name = "Test"
        io = IO(**dict(zip(args[::2], args[1::2])))
        counter = TestCounter(5)
        counter.name = "counter"
        wire(counter.O, io.O)
        wire(counter.COUT, io.COUT)

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
    out, err = capsys.readouterr()
    assert(err == "")
    assert(out == "")

    console.runcmd("p self.O")
    assert get_out(capsys) == "1"

    console.runcmd("next")
    console.runcmd("p self.O")
    assert get_out(capsys) == "2"

    console.runcmd("p self.counter.O")
    assert get_out(capsys) == "2"

    console.runcmd("p self.counter.reg.O")
    assert get_out(capsys) == "2"
    m.config.set_debug_mode(False)
