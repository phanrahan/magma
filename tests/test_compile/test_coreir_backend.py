import magma as m


def test_namespace_collision():
    # global namespace add shouldn't collide with coreir lib add
    @m.combinational2()
    def add(x: m.UInt[16], y: m.UInt[16]) -> m.UInt[16]:
        return x + y

    m.compile("build/add", add.circuit_definition)
