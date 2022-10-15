import magma as m

from examples import complex_when_lazy_tuple


def test_mlir_compiler_finalize_when_order():
    m.compile(
        "build/complex_when_lazy_tuple",
        complex_when_lazy_tuple,
        output="mlir",
    )
