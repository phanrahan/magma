import os


import magma as m
from magma.passes import DefinitionPass


class InsertPrefix(DefinitionPass):
    """
    Insert `prefix` before the names of all circuits
    """

    def __init__(self, main, prefix):
        super().__init__(main)
        self.prefix = prefix

    def __call__(self, definition):
        type(definition).rename(definition, self.prefix + definition.name)



def test_rename_prefix_pass():
    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))

    class Bar(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
        io.O @= Foo()(io.I)

    class Main(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
        io.O @= Bar()(io.I)


    InsertPrefix(Main, "baz_").run()

    m.compile("build/test_rename_prefix_pass", Main)
    verilog_file = os.path.join(os.path.dirname(__file__), "build",
                                "test_rename_prefix_pass.v")
    modules = m.define_from_verilog_file(verilog_file)
    prefix = "baz_"
    for module in modules:
        assert module.name[:len(prefix)] == prefix
