import magma as m


class _GrandChildBuilder(m.CircuitBuilder):
    def __init__(self, name):
        super().__init__(name)
        self._initialize()

    @m.builder_method
    def _initialize(self):
        self._add_port("I", m.In(m.Bit))
        self._add_port("O", m.Out(m.Bit))
        m.wire(self._port("I"), self._port("O"))

    def _finalize(self):
        print (f"Hey I'm {self._name} and finalizing!")


class _PassThroughBuilder(m.CircuitBuilder):
    def __init__(self, name):
        super().__init__(name)
        self._added = False

    @m.builder_method
    def add(self):
        if self._added:
            return
        self._add_port("I", m.In(m.Bit))
        self._add_port("O", m.Out(m.Bit))
        grand_child = _GrandChildBuilder("my_gc")
        m.wire(self._port("I"), grand_child.I)
        m.wire(~grand_child.O, self._port("O"))

    def _finalize(self):
        print (f"Hey I'm {self._name} and finalizing!")


def test_basic():

    class _Top(m.Circuit):
        io = m.IO(x=m.In(m.Bit), y=m.Out(m.Bit))

        builder = _PassThroughBuilder(name="my_pt")
        builder.add()

        builder.I @= io.x
        io.y @= builder.O

    print (repr(_Top))
    m.compile("build/builder_top", _Top, output="coreir")
