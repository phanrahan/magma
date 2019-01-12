import magma as m


def pytest_generate_tests(metafunc):
    if 'target' in metafunc.fixturenames:
        metafunc.parametrize("target", ["verilog", "coreir"])


def test_seq_simple(target):
    @m.circuit.sequential
    class Basic:
        def __init__(self):
            self.x = m.bits(0, 2)
            self.y = m.bits(0, 4)

        def __call__(self, I: m.Bits(2)):
            O = self.y
            self.y[2:] = self.y[:2]
            self.y[:2] = self.x
            self.x = I
            return O

    m.compile(f"build/test_basic", Basic, output=target)
