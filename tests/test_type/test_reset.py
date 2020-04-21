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

    m.compile("build/Bar", Bar, "coreir-verilog", output_intermediate=True)
    assert check_files_equal(__file__, f"build/Bar.json",
                             f"gold/Bar.json")
    assert check_files_equal(__file__, f"build/Bar.v",
                             f"gold/Bar.v")
