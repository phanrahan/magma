import magma as m
from magma.testing.utils import check_gold

from stopwatch import top


def test_stopwatch_compile():
    m.compile("build/stopwatch", top, output="mlir")
    assert check_gold(__file__, "stopwatch.mlir")
