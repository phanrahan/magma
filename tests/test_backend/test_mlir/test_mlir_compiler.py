import tempfile
import magma as m

from examples import complex_when_lazy_tuple


def test_mlir_compiler_finalize_when_order():
    with tempfile.TemporaryDirectory() as tmpdir:
        m.compile(
            f"{tmpdir}/complex_when_lazy_tuple",
            complex_when_lazy_tuple,
            output="mlir",
        )
