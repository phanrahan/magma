import dataclasses
import io
import os
import pathlib
import subprocess
import sys
from typing import List, Optional

from magma.backend.mlir.common import try_call
from magma.backend.mlir.errors import MlirCompilerError
from magma.config import config, EnvConfig
from magma.logging import root_logger


config._register(circt_home=EnvConfig("CIRCT_HOME", "./circt"))

_logger = root_logger().getChild("mlir_backend")


class MlirToVerilogError(MlirCompilerError):
    pass


@dataclasses.dataclass
class MlirToVerilogOpts:
    location_info_style: str = "plain"


def _circt_home() -> pathlib.Path:
    return pathlib.Path(config.circt_home).resolve()


def _circt_opt_binary(circt_home: pathlib.Path) -> pathlib.Path:
    return circt_home / "build/bin/circt-opt"


def _circt_opt_cmd(
        circt_home: pathlib.Path,
        opts: MlirToVerilogOpts,
) -> List[str]:
    bin_ = f"{_circt_opt_binary(circt_home)}"
    passes = [
        "--lower-seq-to-sv",
        "--canonicalize",
        "--hw-cleanup",
        "--prettify-verilog",
        "--export-verilog",
    ]
    extra_opts = [
        "-o=/dev/null",
    ]
    return [bin_] + passes + extra_opts


def _run_subprocess(args, stdin, stdout) -> int:
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
    return proc.returncode


def _make_stream(filename, mode, default):
    if filename is None:
        return default, False
    return open(filename, mode), True


def circt_opt_binary_exists() -> bool:
    circt_home = _circt_home()
    circt_opt_binary = _circt_opt_binary(circt_home)
    # NOTE(rsetaluri): We could simply check for the existence of the file in
    # the filesystem, but instead we actually run the binary and (a) check that
    # it exists (by catching FileNotFoundError), and (b) that it is executable
    # with a basic '--help' interface. Also, temporary buffers are passed for
    # stdin/stdout since we do not care to access them.
    try:
        returncode = _run_subprocess(
            [circt_opt_binary, "--help"],
            stdin=io.BytesIO(),
            stdout=io.BytesIO(),
        )
    except FileNotFoundError:
        return False
    return returncode == 0


def mlir_to_verilog(
        istream: io.RawIOBase,
        ostream: io.RawIOBase = sys.stdout,
        opts: MlirToVerilogOpts = MlirToVerilogOpts(),
):
    circt_home = _circt_home()
    cmd = _circt_opt_cmd(circt_home, opts)
    _logger.info(f"Running cmd: {' '.join(cmd)}")
    returncode = _run_subprocess(cmd, istream, ostream)
    if returncode != 0:
        cmd_str = " ".join(cmd)
        raise MlirToVerilogError(
            f"Error running {cmd_str}, got returncode {returncode}"
        )
