import magma as m


class SimpleGenerator(m.GeneratorBase):
    width: int = 16

    def elaborate(self):
        class _Simple(m.Circuit):
            IO = ["I", m.In(m.Bits[self.width]),
                  "O", m.Out(m.Bits[self.width]),]
            name = f"Simple{self.width}"

            @classmethod
            def definition(io):
                m.wire(io.O, io.I)

        return _Simple


def test_simple_generator():
    gen = SimpleGenerator(width=10)

    # Check a simple invocation of the generator.
    Simple10 = gen.elaborate()
    assert repr(Simple10) == """\
Simple10 = DefineCircuit("Simple10", "I", In(Bits[10]), "O", Out(Bits[10]))
wire(Simple10.I, Simple10.O)
EndCircuit()"""

    # Check that changing the parameter on the generator instance results in the
    # correct elaboration.
    gen.width = 20
    Simple20 = gen.elaborate()
    assert repr(Simple20) == """\
Simple20 = DefineCircuit("Simple20", "I", In(Bits[20]), "O", Out(Bits[20]))
wire(Simple20.I, Simple20.O)
EndCircuit()"""

    # Check that caching works as expected.
    assert Simple20 is not Simple10
    gen.width = 10
    assert gen.elaborate() is Simple10
