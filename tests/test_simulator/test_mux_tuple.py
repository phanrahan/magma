import magma as m
from magma.bitutils import clog2
from hwtypes import BitVector
from magma.simulator import PythonSimulator


def _declare_muxn(height, width):
    def _simulate(self, value_store, state_store):
        sel = BitVector[clog2(height)](value_store.get_value(self.I.sel))
        out = BitVector[width](value_store.get_value(self.I.data[int(sel)]))
        value_store.set_value(self.O, out)

    I_fields = dict(data=m.Array[height, m.Bits[width]],
                    sel=m.Bits[clog2(height)])

    class _Mux(m.Circuit):
        name = f"mux{height}x{width}"
        io = m.IO(I=m.In(m.Product.from_fields("anon", I_fields)),
                  O=m.Out(m.Bits[width]))
        primitive = True
        stateful = False
        simulate = _simulate

    return _Mux


def test_muxn():
    class Main(m.Circuit):
        io = m.IO(I0=m.In(m.Bits[5]),
                  I1=m.In(m.Bits[5]),
                  S=m.In(m.Bits[1]),
                  O=m.Out(m.Bits[5]))

        in_ = m.product(data=m.array([io.I0, io.I1]), sel=io.S)
        io.O @= _declare_muxn(2, 5)()(in_)

    sim = PythonSimulator(Main)
    for i in range(5):
        I0 = BitVector.random(5)
        I1 = BitVector.random(5)
        S = BitVector.random(1)
        sim.set_value(Main.I0, I0)
        sim.set_value(Main.I1, I1)
        sim.set_value(Main.S, S)
        sim.evaluate()
        assert sim.get_value(Main.O) == (I1 if S else I0)
