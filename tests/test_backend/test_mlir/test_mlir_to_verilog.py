import io
import pathlib
import pytest
import tempfile
import textwrap
from typing import Optional

import circt

import magma as m
from magma.backend.mlir.mlir_to_verilog import (
    mlir_to_verilog,
    MlirToVerilogOpts,
)


def _run_test(input_: Optional[str] = None, **kwargs):
    istream = io.TextIOWrapper(io.BytesIO())
    ostream = io.TextIOWrapper(io.BytesIO())
    if input_ is not None:
        istream.write(input_)
        istream.seek(0)
    opts = MlirToVerilogOpts(**kwargs)
    mlir_to_verilog(istream, ostream, opts)
    return istream, ostream


def test_basic():
    _, __ = _run_test()


def test_module():
    _, ostream = _run_test("module {}\n")
    ostream.seek(0)
    assert (
        ostream.read() == (
            "// Generated by CIRCT firtool-1.51.0-75-gbecb4c0ef\n"
        )
    )


def test_bad_input():
    with pytest.raises(circt.ir.MLIRError):
        _run_test("blahblahblah")


@pytest.mark.parametrize("style", ("plain", "wrapInAtSquareBracket", "none"))
def test_location_info_style(style):
    ir = textwrap.dedent(
        """
        module attributes {{circt.loweringOptions = "locationInfoStyle={style}"}} {{
          hw.module @M() -> () {{}}
        }}
        """
    )
    ir = ir.format(style=style)
    _, ostream = _run_test(ir)
    ostream.seek(0)
    ostream.readline()  # skip header
    line = ostream.readline().rstrip()
    expected = "module M();"
    if style == "plain":
        expected += "	// -:3:3"
    elif style == "wrapInAtSquareBracket":
        expected += "	// @[-:3:3]"
    assert line == expected


@pytest.mark.parametrize("explicit_bitcast", (False, True))
def test_explicit_bitcast(explicit_bitcast):
    explicit_bitcast_attr = ",explicitBitcast" if explicit_bitcast else ""
    ir = textwrap.dedent(
        """
        module attributes {{circt.loweringOptions = "locationInfoStyle=none{explicit_bitcast_attr}"}} {{
            hw.module @M(%a: i8, %b: i8) -> (y: i8) {{
              %0 = comb.add %a, %b : i8
              hw.output %0 : i8
            }}
        }}
        """
    )
    ir = ir.format(explicit_bitcast_attr=explicit_bitcast_attr)
    _, ostream = _run_test(ir)
    ostream.seek(0)
    # Skip first 6 lines (incl. header).
    for _ in range(7):
        ostream.readline()
    line = ostream.readline().strip()
    if not explicit_bitcast:
        expected = "assign y = a + b;"
    else:
        expected = "assign y = 8'(a + b);"
    assert line == expected


@pytest.mark.parametrize("disallow_expression_inlining_in_ports", (False, True))
def test_disallow_expression_inlining_in_ports(disallow_expression_inlining_in_ports):
    disallow_expression_inlining_in_ports_attr = (
        ",disallowExpressionInliningInPorts"
        if disallow_expression_inlining_in_ports
        else ""
    )

    ir = textwrap.dedent(
        """
        module attributes {{circt.loweringOptions = "locationInfoStyle=none{disallow_expression_inlining_in_ports_attr}"}} {{
          hw.module.extern @Foo(%I: i1) -> (O: i1)
          hw.module @M(%I: i1) -> (O: i1) {{
              %1 = hw.constant -1 : i1
              %0 = comb.xor %1, %I : i1
              %2 = hw.instance "foo" @Foo(I: %0: i1) -> (O: i1)
              hw.output %2 : i1
          }}
        }}
        """
    )
    ir = ir.format(
        disallow_expression_inlining_in_ports_attr=disallow_expression_inlining_in_ports_attr
    )
    _, ostream = _run_test(ir)
    ostream.seek(0)
    found = False
    while True:
        line = ostream.readline().strip()
        if line.startswith(".I"):
            found = True
            break
    assert found
    if not disallow_expression_inlining_in_ports_attr:
        assert line == ".I (~I),"
    else:
        assert line == ".I (_foo_I),"


@pytest.mark.parametrize("omit_version_comment", (False, True))
def test_omit_version_comment(omit_version_comment):
    omit_version_comment_attr = (
        ",omitVersionComment"
        if omit_version_comment
        else ""
    )

    ir = textwrap.dedent(
        """
        module attributes {{circt.loweringOptions = "locationInfoStyle=none{omit_version_comment_attr}"}} {{
          hw.module @M() -> () {{}}
        }}
        """
    )
    ir = ir.format(
        omit_version_comment_attr=omit_version_comment_attr
    )
    _, ostream = _run_test(ir)
    ostream.seek(0)
    first = ostream.readline().strip()
    if omit_version_comment_attr:
        assert first == "module M();"
    else:
        assert first.startswith("// Generated by")


@pytest.mark.parametrize("specify_output_file", (False, True))
def test_split_verilog(specify_output_file):
    ir = textwrap.dedent(
        """
        module attributes {{circt.loweringOptions = "locationInfoStyle=none"}} {{
          hw.module @M() -> () {attribute_string} {{}}
        }}
        """
    )
    with tempfile.TemporaryDirectory() as tempdir:
        output_file = f"{tempdir}/outfile.sv"
        if specify_output_file:
            attribute_string = (
                f"attributes "
                f"{{output_file = #hw.output_file<\"{output_file}\">}}"
            )
        else:
            attribute_string = ""
        ir = ir.format(attribute_string=attribute_string)
        opts = {"split_verilog": True}
        if not specify_output_file:
            opts["split_verilog_directory"] = tempdir
        _, ostream = _run_test(ir, **opts)
        ostream.seek(0)
        # We expect the output to be empty due to split verilog.
        assert not ostream.readline()

        # Now read ostream from the expcted output file. If the output file is
        # not specificed explicitly, then it goes into <split verilog
        # directory>/<module name>.sv (in this case, <tempdir>/M.sv).
        if not specify_output_file:
            output_file = f"{tempdir}/M.sv"
        with open(output_file, "r") as ostream:
            ostream.readline()  # skip header
            assert ostream.readline().rstrip() == "module M();"
            assert ostream.readline().rstrip() == "endmodule"
