import magma as m
import pytest
from magma.testing import check_files_equal


def test_asyncreset_n():
    class Foo(m.Circuit):
        IO = m.ClockInterface(has_async_resetn=True)

    class Bar(m.Circuit):
        IO = m.ClockInterface(has_async_resetn=True)

        @classmethod
        def definition(io):
            # asyncresetn ports should be automatically connected in the
            # backend
            foo = Foo()

    m.compile("build/Foo", "coreir-verilog")
    assert check_files_equal(__file__, f"build/Foo.v",
                             f"gold/Foo.v")
