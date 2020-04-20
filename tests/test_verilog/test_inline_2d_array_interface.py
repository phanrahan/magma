import magma as m
from magma.testing import check_files_equal
import os


def test_inline_2d_array_interface():
    class Main(m.Generator):
        @staticmethod
        def generate(width, depth):
            class MonitorWrapper(m.Circuit):
                io = m.IO(arr=m.In(m.Array[depth, m.Bits[width]]))

                m.inline_verilog("""
monitor #(.WIDTH({width}), .DEPTH({depth})) monitor_inst(.arr({arr}));
                    """, width=width, depth=depth, arr=io.arr)

            return MonitorWrapper

    m.compile("build/test_inline_2d_array_interface",
              Main.generate(8, 64))
    assert check_files_equal(__file__,
                             f"build/test_inline_2d_array_interface.v",
                             f"gold/test_inline_2d_array_interface.v")
    file_dir = os.path.abspath(os.path.dirname(__file__))
    assert not os.system("verilator --lint-only "
                         f"{file_dir}/build/test_inline_2d_array_interface.v "
                         f"{file_dir}/vsrc/2d_array_interface.v "
                         "--top-module MonitorWrapper")
