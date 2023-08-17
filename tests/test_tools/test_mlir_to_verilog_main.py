import pathlib
import tempfile
import textwrap

from tools.mlir_to_verilog_main import main


def test_basic():

    with tempfile.TemporaryDirectory() as tempdir:
        tempdir = pathlib.Path(tempdir)
        infile = tempdir / "infile.mlir"
        with open(infile, "w") as f:
            f.write("module {}\n")
        outfile = tempdir / "outfile.v"
        main([str(infile), "--outfile", str(outfile)])
        assert outfile.is_file()

    
