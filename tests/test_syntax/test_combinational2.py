import tempfile
import os
import inspect

from hwtypes import BitVector, Bit
import ast_tools

import magma as m
from magma.testing import check_files_equal


def test_combinational2_basic_if():
    @m.combinational2()
    def basic_if(I: m.Bits[2], S: m.Bit) -> m.Bit:
        if S:
            return I[0]
        else:
            return I[1]

    class Main(m.Circuit):
        io = m.IO(I=m.In(m.Bits[2]), S=m.In(m.Bit), O=m.Out(m.Bit))
        io.O @= basic_if(io.I, io.S)

    m.compile("build/test_combinational2_basic_if", Main, inline=True)
    assert check_files_equal(__file__, f"build/test_combinational2_basic_if.v",
                             f"gold/test_combinational2_basic_if.v")

    # Test function call interface for python values
    assert basic_if(BitVector[2](2), Bit(0)) == 1
    assert basic_if(BitVector[2](2), Bit(1)) == 0


def test_pre_post_passes(capsys):
    with tempfile.TemporaryDirectory() as tmpdir:
        l0 = inspect.currentframe().f_lineno + 1

        @m.combinational2(pre_passes=[ast_tools.passes.loop_unroll()],
                          post_passes=[
                              ast_tools.passes.debug(dump_source_filename=True,
                                                     dump_source_lines=True)],
                          env=locals().update(y=3),
                          debug=True, path=tmpdir, file_name="foo.py")
        def pre_unroll(I: m.Bits[3]) -> m.Bits[3]:
            for j in ast_tools.macros.unroll(range(y)):
                if I[j]:
                    return m.Bits[3](j)
            return m.Bits[3](4)
        with open(os.path.join(tmpdir, "foo.py"), "r") as output:
            assert output.read() == """\
def pre_unroll(I: m.Bits[3]) -> m.Bits[3]:
    _cond_0 = _auto_name_0("_cond_0", I[0])
    __0_return_0 = _auto_name_0("__0_return_0", m.Bits[3](0))
    _cond_1 = _auto_name_0("_cond_1", I[1])
    __0_return_1 = _auto_name_0("__0_return_1", m.Bits[3](1))
    _cond_2 = _auto_name_0("_cond_2", I[2])
    __0_return_2 = _auto_name_0("__0_return_2", m.Bits[3](2))
    __0_return_3 = _auto_name_0("__0_return_3", m.Bits[3](4))
    return __phi(_cond_0, __0_return_0, __phi(_cond_1, __0_return_1, __phi(_cond_2, __0_return_2, __0_return_3)))
"""

    assert capsys.readouterr().out == f"""\
BEGIN SOURCE_FILENAME
{os.path.abspath(__file__)}
END SOURCE_FILENAME

BEGIN SOURCE_LINES
{l0+1}:        @m.combinational2(pre_passes=[ast_tools.passes.loop_unroll()],
{l0+2}:                          post_passes=[
{l0+3}:                              ast_tools.passes.debug(dump_source_filename=True,
{l0+4}:                                                     dump_source_lines=True)],
{l0+5}:                          env=locals().update(y=3),
{l0+6}:                          debug=True, path=tmpdir, file_name="foo.py")
{l0+7}:        def pre_unroll(I: m.Bits[3]) -> m.Bits[3]:
{l0+8}:            for j in ast_tools.macros.unroll(range(y)):
{l0+9}:                if I[j]:
{l0+10}:                    return m.Bits[3](j)
{l0+11}:            return m.Bits[3](4)
END SOURCE_LINES

"""

    m.compile("build/test_combinational2_pre_post_passes",
              pre_unroll.circuit_definition, inline=True)
    assert check_files_equal(__file__,
                             f"build/test_combinational2_pre_post_passes.v",
                             f"gold/test_combinational2_pre_post_passes.v")


def test_temporary_driver_repr():

    def f3(I: m.Bit) -> m.Tuple[m.Bit]:
        if I == 0:
            O = m.Bit(0)
        else:
            O = m.Bit(1)
        return m.tuple_([O])

    f3 = m.combinational2()(f3)
    repr(f3.circuit_definition)
