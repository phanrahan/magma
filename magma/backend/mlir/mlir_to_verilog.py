import io
import os
import pathlib
import subprocess
import sys
from typing import List, Optional

from magma.backend.mlir.common import try_call
from magma.config import config, EnvConfig


config._register(circt_home=EnvConfig("CIRCT_HOME", "./circt"))


def _get_circt_home() -> pathlib.Path:
    return pathlib.Path(config.circt_home).resolve()


def _make_opt_cmd(circt_home: pathlib.Path) -> List[str]:
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


def _make_stream(filename, mode, default):
    if filename is None:
        return default, False
    return open(filename, mode), True


def mlir_to_verilog(istream: io.RawIOBase, ostream: io.RawIOBase = sys.stdout):
    circt_home = _get_circt_home()
    opt_cmd = _make_opt_cmd(circt_home)
    _subprocess_run(opt_cmd, istream, ostream)


def main(infile: Optional[str] = None, outfile: Optional[str] = None):
    istream, close_istream = _make_stream(infile, "r", sys.stdin)
    ostream, close_ostream = _make_stream(outfile, "w", sys.stdout)
    ret = mlir_to_verilog(istream, ostream)
    assert ret is None
    if close_istream:
        istream.close()
    if close_ostream:
        ostream.close()
