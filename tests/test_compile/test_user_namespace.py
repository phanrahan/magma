import magma as m
from magma.testing import check_files_equal


def _make_io(T):
    return m.IO(I=m.In(T), O=m.Out(T))


def _make_top(T):
    class _Decl(m.Circuit):
        io = _make_io(T)

    class _Bar(m.Circuit):
        name = "Bar"
        io = _make_io(T)
        io.O @= _Decl()(io.I)

    class _Foo(m.Circuit):
        name = "Foo"
        io = _make_io(T)
        io.O @= _Bar()(io.I)

    return _Foo


def test_basic():
    top = _make_top(m.Bit)
    name = "test_user_namespace_basic"
    m.compile(f"build/{name}", top, output="coreir",
              user_namespace="my_namespace")
    assert check_files_equal(__file__,
                             f"build/{name}.json",
                             f"gold/{name}.json")


def test_passes():
    T = m.Product.from_fields("anonymous", dict(x=m.Bit, y=m.Bit))
    top = _make_top(T)
    name = "test_user_namespace_passes"
    passes = ["flattentypes"]
    m.compile(f"build/{name}", top, output="coreir",
              passes=passes,
              user_namespace="my_namespace")
    assert check_files_equal(__file__,
                             f"build/{name}.json",
                             f"gold/{name}.json")


def test_verilog_prefix():
    T = m.Product.from_fields("anonymous", dict(x=m.Bit, y=m.Bit))
    top = _make_top(T)
    name = "test_user_namespace_verilog_prefix"
    m.compile(f"build/{name}", top, output="coreir-verilog",
              user_namespace="my_namespace")
    assert check_files_equal(__file__, f"build/{name}.v", f"gold/{name}.v")


def test_user_namespace_override():
    class Foo(m.Circuit):
        io = _make_io(m.Bit)
        namespace = "global"  # override user_namespace option

    class Main(m.Circuit):
        io = _make_io(m.Bit)
        io.O @= Foo()(io.I)

    name = "test_user_namespace_override"
    m.compile(f"build/{name}", Main, user_namespace="my_namespace")

    assert check_files_equal(__file__,
                             f"build/{name}.v",
                             f"gold/{name}.v")
