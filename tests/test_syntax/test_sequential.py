import magma as m


def pytest_generate_tests(metafunc):
    if 'target' in metafunc.fixturenames:
        metafunc.parametrize("target", ["coreir"])


def test_seq_simple(target):
    @m.circuit.sequential
    class Basic:
        def __init__(self):
            self.x: m.Bits(2) = m.bits(0, 2)
            self.y: m.Bits(2) = m.bits(0, 2)

        def __call__(self, I: m.Bits(2)) -> m.Bits(2):
            O = self.y
            self.y = self.x
            self.x = I
            return O

    m.compile(f"build/test_seq_simple", Basic, output=target)
