import magma as m
from magma.simulator import PythonSimulator


def test_product_python_sim_basic():
    class T(m.Product):
        a = m.Bits[4]
        b = m.Bits[4]

    class Main(m.Circuit):
        io = m.IO(I=m.In(T), O=m.Out(T))

        io.O @= io.I

    simulator = PythonSimulator(Main)
    simulator.set_value(Main.I.a, 5)
    simulator.set_value(Main.I.b, 11)
    simulator.evaluate()
    assert simulator.get_value(Main.I.a) == 5
    assert simulator.get_value(Main.I.b) == 11
