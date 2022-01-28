import io
import os
import pathlib
import subprocess
import sys
from typing import List, Optional

from magma.backend.mlir.common import try_call


def get_circt_home() -> pathlib.Path:
    circt_home = os.environ.get("CIRCT_HOME", "../circt/")
    return pathlib.Path(circt_home).resolve()


def make_opt_cmd(circt_home: pathlib.Path) -> List[str]:
    opt = circt_home / "build/bin/circt-opt"
    return [
        f"{opt}", "--lower-seq-to-sv", "--canonicalize", "--hw-cleanup",
        "--prettify-verilog", "--export-verilog", "-o=/dev/null",
    ]


def _subprocess_run(args, stdin, stdout):
    stdin_pipe = (
        try_call(lambda: stdin.fileno(), io.UnsupportedOperation) is None
    )
    stdout_pipe = (
        try_call(lambda: stdout.fileno(), io.UnsupportedOperation) is None
    )
    stdin_actual = subprocess.PIPE if stdin_pipe else stdin
    stdout_actual = subprocess.PIPE if stdout_pipe else stdout
    proc = subprocess.Popen(args, stdin=stdin_actual, stdout=stdout_actual)
    if stdin_pipe:
        proc.stdin.write(stdin.read())
        proc.stdin.close()
    proc.wait()
    if stdout_pipe:
        stdout.write(proc.stdout.read())


def mlir_to_verilog(istream: io.RawIOBase, ostream: io.RawIOBase = sys.stdout):
    circt_home = get_circt_home()
    opt_cmd = make_opt_cmd(circt_home)
    _subprocess_run(opt_cmd, istream, ostream)


def main(infile: Optional[str] = None, outfile: Optional[str] = None):
    if infile is None:
        istream = sys.stdin
        close_istream = False
    else:
        istream = open(infile, "r")
        close_istream = True
    if outfile is None:
        ostream = sys.stdout
        close_ostream = False
    else:
        ostream = open(outfile, "w")
        close_ostream = True
    ret = mlir_to_verilog(istream, ostream)
    assert ret is None
    if close_istream:
        istream.close()
    if close_ostream:
        ostream.close()
