from .test_primitives import *
from magma.simulator import PythonSimulator
from magma import *
from magma.passes.clock import drive_undriven_other_clock_types_in_inst
from magma.scope import *

def test():
    def FFs(n):
        return [PRIM_FF() for i in range(n)]

    def Register(n):
        args = ["I", In(Array[n, Bit]), "O", Out(Array[n, Bit])] + ClockInterface(False, False, False)

        class RegCircuit(Circuit):
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
        wire(counter.O, io.O)
        wire(counter.COUT, io.COUT)

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
