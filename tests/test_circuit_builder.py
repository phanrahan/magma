import magma as m


class _PassThroughBuilder(m.CircuitBuilder):
    def __init__(self, name):
        super().__init__(name)
        self._added = False

    @m.builder_method
    def add(self):
        if self._added:
            return
        self._add("I", m.In(m.Bit))
        self._add("O", m.Out(m.Bit))
        m.wire(~self._port("I"), self._port("O"))


def test_basic():

    class _Top(m.Circuit):
        io = m.IO(x=m.In(m.Bit), y=m.Out(m.Bit))

        builder = _PassThroughBuilder(name="my_pt")
        builder.add()

        builder.I @= io.x
        io.y @= builder.O

    print (_Top._context_._builders)
    print (repr(_Top))

    m.compile("_Top", _Top, output="coreir")
