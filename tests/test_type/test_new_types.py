import magma as m
import pytest
from magma.testing import check_files_equal


@pytest.mark.parametrize('output', ['coreir-verilog', 'coreir'])
def test_new_types(output):
    # TODO: Make it easier to do a type alias like this (for a parametrized type)
    def Coordinate(num_bits):
        return m.Bits[num_bits]

    # Parametrized types should be implemented using a type constructure
    # TODO: Add suport for isinstance(t, Polygon), need to rework to use class
    # structure or at least autogenerate a PolygonType (or document how to
    # subclass and create a new Type/Kind)
    def Point2D(num_bits):
        class Point2D(m.Product):
            x = Coordinate(num_bits)
            y = Coordinate(num_bits)

        return Point2D

    def Polygon(num_vertices, num_bits):
        return m.Array[num_vertices, Point2D(num_bits)]

    class TestCircuit(m.Circuit):
        io = m.IO(
            I=m.In(Polygon(12, 3)),
            O=m.Out(Polygon(12, 3))
        )
        m.wire(io.I, io.O)

    suffix = 'v' if output == 'coreir-verilog' else 'json'
    m.compile('build/test_new_types', TestCircuit, output=output)
    assert check_files_equal(__file__, f"build/test_new_types.{suffix}",
                             f"gold/test_new_types.{suffix}")
