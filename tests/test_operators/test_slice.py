import magma as m
from magma.testing import check_files_equal


def test_slice_fixed_range():
	class TestSlice(m.Circuit):
		IO = [
			"I", m.In(m.Bits[10]), 
			"x", m.In(m.Bits[2]), 
			"O", m.Out(m.Bits[6])
		]

		@classmethod
		def definition(io):
			io.O @= m.slice(io.I, start=io.x, width=6)

	m.compile("build/TestSlice", TestSlice)
	assert check_files_equal(__file__,
                             "build/TestSlice.v",
                             "gold/TestSlice.v")
