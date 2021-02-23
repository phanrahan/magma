import magma as m
from magma.testing import check_files_equal


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
        self._set_definition_attr("_some_private_attr", None)

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
        # Check set_instance_name() API.
        builder.set_instance_name("my_pt_0")

        builder.I @= io.x
        io.y @= builder.O

    assert repr(_Top) == """\
_Top = DefineCircuit("_Top", "x", In(Bit), "y", Out(Bit))
my_pt_0 = my_pt("I", my_pt_0.I, "O", my_pt_0.O)
wire(_Top.x, my_pt_0.I)
wire(my_pt_0.O, _Top.y)
EndCircuit()"""
    m.compile("build/test_circuit_builder_basic", _Top, output="coreir")
    assert check_files_equal(__file__,
                             "build/test_circuit_builder_basic.json",
                             "gold/test_circuit_builder_basic.json")
    # Check _set_definition_attr.
    assert len(_Top.instances) == 1
    inst = _Top.instances[0]
    assert inst.name == "my_pt_0"
    defn = type(inst)
    assert defn.name == "my_pt"
    assert defn._some_private_attr == None

    # Check defn property.
    assert defn is _Top.builder.defn

    # Check that re-instantiation of builder defn works.
    class _:
        defn()


def test_dont_instantiate():
    builder = _PassThroughBuilder(name="my_pt")
    builder.add()
    builder.finalize(dont_instantiate=True)
    assert repr(builder.defn) == """\
my_pt = DefineCircuit("my_pt", "I", Out(Bit), "O", In(Bit))
magma_Bit_not_inst0 = magma_Bit_not()
my_gc = my_gc("I", my_gc.I, "O", my_gc.O)
wire(my_gc.O, magma_Bit_not_inst0.in)
wire(my_pt.I, my_gc.I)
wire(magma_Bit_not_inst0.out, my_pt.O)
EndCircuit()"""
