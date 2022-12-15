import pytest
import magma as m
from magma.config import config
from magma.testing.utils import check_gold


@pytest.fixture(autouse=True)
def use_namer_dict():
    config.use_namer_dict = True
    yield
    config.use_namer_dict = False


def test_basic_namer_dict():

    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bits[8]), O=m.Out(m.Bits[8]))

    class test_basic_namer_dict(m.Circuit):
        io = m.IO(I=m.In(m.Bits[8]), O=m.Out(m.Bits[8]))
        foo = Foo()
        assert foo.name == "foo"
        x = m.Bits[8]()
        assert x.name.name == "x"
        x @= io.I
        io.O @= foo(x)

    m.compile("build/test_basic_namer_dict", test_basic_namer_dict,
              output="mlir")
    assert check_gold(__file__, f"test_basic_namer_dict.mlir")


def test_namer_dict_multiple():

    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bits[8]), O=m.Out(m.Bits[8]))

    class test_namer_dict_multiple(m.Circuit):
        io = m.IO(I=m.In(m.Bits[8]), O=m.Out(m.Bits[8]))
        foo = Foo()
        x = m.Bits[8]()
        x @= io.I
        y = foo(x)
        foo = Foo()
        x = m.Bits[8]()
        x @= y
        io.O @= foo(x)

    m.compile("build/test_namer_dict_multiple", test_namer_dict_multiple,
              output="mlir")
    assert check_gold(__file__, f"test_namer_dict_multiple.mlir")


def test_namer_dict_smart_bits():

    class test_namer_dict_smart_bits(m.Circuit):
        io = m.IO(I0=m.In(m.smart.SmartBits[8]),
                  I1=m.In(m.smart.SmartBits[8]),
                  O=m.Out(m.smart.SmartBits[9]))
        x = m.smart.SmartBits[9]()
        x @= io.I0 + io.I1
        io.O @= x

    m.compile("build/test_namer_dict_smart_bits", test_namer_dict_smart_bits,
              output="mlir")
    assert check_gold(__file__, f"test_namer_dict_smart_bits.mlir")


def test_namer_dict_already_named():

    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bits[8]), O=m.Out(m.Bits[8]))

    class test_namer_dict_already_named(m.Circuit):
        io = m.IO(I=m.In(m.Bits[8]), O=m.Out(m.Bits[8]))
        foo = Foo(name="bar")
        assert foo.name == "bar"
        x = m.Bits[8](name="y")
        assert x.name.name == "y"
        x @= io.I
        io.O @= foo(x)

    m.compile("build/test_namer_dict_already_named",
              test_namer_dict_already_named, output="mlir")
    assert check_gold(__file__, f"test_namer_dict_already_named.mlir")


def test_namer_dict_generator():

    class Foo(m.Generator2):
        def __init__(self, n):
            self.io = m.IO(I=m.In(m.Bits[n]), O=m.Out(m.Bits[n]))
            self.x = m.Bits[n]()
            self.x @= self.io.I
            self.io.O @= self.x

    m.compile("build/test_namer_dict_generator", Foo(8), output="mlir")
    assert check_gold(__file__, f"test_namer_dict_generator.mlir")
