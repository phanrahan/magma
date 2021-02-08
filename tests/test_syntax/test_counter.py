import magma as m
from magma.simulator import PythonSimulator
from magma.simulator.coreir_simulator import CoreIRSimulator
from hwtypes import BitVector as BV


def test_counter():
    @m.sequential2()
    class Counter:
        def __init__(self):
            self.count = m.Register(m.UInt[16])()

        def __call__(self, inc : m.Bit) -> m.UInt[16]:
            if inc:
                self.count = self.count + 1

            O = self.count
            return O
    print(repr(Counter))

    sim = PythonSimulator(Counter, Counter.CLK)
    sim.set_value(Counter.inc, True)
    sim.evaluate()
    for i in range(4):
        assert sim.get_value(Counter.O) == i + 1
        sim.advance_cycle()
    sim.set_value(Counter.inc, False)
    sim.evaluate()
    for i in range(4):
        assert sim.get_value(Counter.O) == 4
        sim.advance_cycle()

    sim = CoreIRSimulator(Counter, Counter.CLK)
    sim.set_value(Counter.inc, 1)
    sim.evaluate()
    for i in range(4):
        assert sim.get_value(Counter.O) == BV[16](i + 1)
        sim.advance_cycle()
    sim.set_value(Counter.inc, 0)
    sim.evaluate()
    for i in range(4):
        assert sim.get_value(Counter.O) == BV[16](4)
        sim.advance_cycle()

if __name__ == "__main__":
    test_counter()
