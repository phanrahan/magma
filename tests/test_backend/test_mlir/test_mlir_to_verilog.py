import io
import pytest
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
            "// Generated by CIRCT unknown git version\n"
        )
    )


def test_bad_input():
    with pytest.raises(circt.ir.MLIRError):
        _run_test("blahblahblah")


@pytest.mark.parametrize("style", ("plain", "wrapInAtSquareBracket", "none"))
def test_location_info_style(style):
    ir = (
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
        expected += "	// -:3:11"
    elif style == "wrapInAtSquareBracket":
        expected += "	// @[-:3:11]"
    assert line == expected


@pytest.mark.parametrize("explicit_bitcast", (False, True))
def test_explicit_bitcast(explicit_bitcast):
    explicit_bitcast_attr = ",explicitBitcast" if explicit_bitcast else ""
    ir = (
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

    ir = (
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

    ir = (
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


def test_split_verilog():
    ir = (
        """
        module attributes {{circt.loweringOptions = "locationInfoStyle=none"}} {{
          hw.module @M() -> () attributes {{output_file = {output_file}}} {{}}
        }}
        """
    )
    output_file = "tests/test_backend/test_mlir/build/test_mlir_to_verilog_split_verilog.sv"
    ir = ir.format(output_file=f"#hw.output_file<\"{output_file}\">")
    _, ostream = _run_test(ir, split_verilog=True)
    ostream.seek(0)
    assert not ostream.readline()  # output expected to be empty

    # Now read ostream from the expcted output file.
    ostream = open(output_file)
    ostream.readline()  # skip header
    assert ostream.readline().rstrip() == "module M();"
    assert ostream.readline().rstrip() == "endmodule"
