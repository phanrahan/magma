import magma as m
from magma.testing import check_files_equal


class _MyMux(m.Generator2):
    cls_level_var = "I like being a mux"

    def __init__(self, width, height):
        self.width = width
        self.height = height
        sel_bits = m.bitutils.clog2(height)
        self.name = f"MyMux{width}x{height}"
        args = {f"I{i}": m.In(m.Bits[width]) for i in range(height)}
        args["O"] = m.Out(m.Bits[width])
        args["S"] = m.In(m.Bits[sel_bits])
        self.io = m.IO(**args)

    def to_string(self):
        return f"{_MyMux.cls_level_var} of {self.width}x{self.height}"


def test_type_relations():
    assert issubclass(_MyMux, m.Generator2)
    assert issubclass(_MyMux, m.DefineCircuitKind)
    MyMux4x4 = _MyMux(4, 4)  # circuit defn.
    assert isinstance(MyMux4x4, m.DefineCircuitKind)
    assert isinstance(MyMux4x4, _MyMux)
    assert issubclass(MyMux4x4, m.Circuit)

    insts = []

    class _(m.Circuit):
        mux = MyMux4x4()
        insts.append(mux)

    mux = insts[0]
    assert isinstance(mux, MyMux4x4)
    assert isinstance(mux, m.Circuit)


def test_properties():
    MyMux4x4 = _MyMux(4, 4)
    assert MyMux4x4.name == "MyMux4x4"
    assert MyMux4x4.width == 4
    assert MyMux4x4.height == 4
    assert MyMux4x4.to_string() == "I like being a mux of 4x4"


def test_compilation():

    class _Top(m.Circuit):
        io = m.IO(x=m.In(m.Bit), y=m.In(m.Bit), z=m.Out(m.Bit))
        mux = _MyMux(1, 2)()
        mux.I0[0] @= io.x
        mux.I1[0] @= io.y
        mux.S @= 0
        io.z @= mux.O[0]

    m.compile("build/TopGen", _Top, output="coreir")
    assert check_files_equal(__file__, "build/TopGen.json", "gold/TopGen.json")


def test_cache():
    MyMux4x8 = _MyMux(4, 8)
    MyMux4x8_other = _MyMux(4, 8)
    assert MyMux4x8 is MyMux4x8_other
    MyMux4x16 = _MyMux(4, 16)
    assert MyMux4x16 is not MyMux4x8


def test_cache_miss():

    # Different class, with same parameters; internals don't matter.
    class _MyOtherMux(m.Generator2):
        def __init__(self, width, height):
            pass

    MyMux4x8 = _MyMux(4, 8)
    MyOtherMux4x8 = _MyOtherMux(4, 8)
    assert MyMux4x8 is not MyOtherMux4x8


def test_no_cache():

    class _MyGen(m.Generator2):
        _cache_ = False

        def __init__(self):
            self.io = m.IO(x=m.In(m.Bit))

    my_gen = _MyGen()
    my_gen_other = _MyGen()
    assert my_gen is not my_gen_other
    assert repr(my_gen) == repr(my_gen_other)


def test_subclass_generator_instance():
    Base = m.Register(m.Bit)

    class MyRegister(Base):
        io = Base.io
        verilog = "Foo"

    assert isinstance(MyRegister, m.Register)
