import magma as m
from magma.testing import check_files_equal
import os
import pytest
import tempfile


@pytest.mark.parametrize("inline", [False, True])
def test_708(inline):
    class A(m.Product):
        x = m.UInt[8]

    @m.sequential2()
    class Test:
        def __init__(self):
            self.a: A = m.product(x=m.uint(0, 8))

        def __call__(self, c: m.Bit) -> m.AnonProduct[dict(a=A)]:
            if c:
                a = m.replace(self.a, dict(x=self.a.x + 1))
            else:
                a = self.a
            return m.product(a=a)

    name = f"test_708_inline_{inline}"
    path = f"build/{name}"
    m.compile(path, Test, output="coreir-verilog", inline=inline,
              disable_width_cast=True, disable_ndarray=inline is False)
    verilator_path = os.path.join(os.path.dirname(__file__), path)
    assert not os.system(
        f"verilator --lint-only --language 1364-2005 {verilator_path}.v"
    )
    assert check_files_equal(__file__, f"{path}.v", f"gold/{name}.v")
