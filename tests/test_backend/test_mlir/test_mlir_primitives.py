from magma.testing.utils import check_gold
import magma as m


def test_mlir_primitive_neg():
    class _Test(m.Circuit):
        name = "test_mlir_primitive_neg"
        io = m.IO(I=m.In(m.SInt[2]), O=m.Out(m.SInt[2]))
        io.O @= -io.I

    m.compile(f"build/{_Test.name}", _Test, output="mlir")
    assert check_gold(__file__, f"{_Test.name}.mlir")
