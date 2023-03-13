import dataclasses
import io
import os
import pathlib
import re
import subprocess
import sys
from typing import List, Optional

from magma.backend.mlir.common import try_call
from magma.backend.mlir.errors import MlirCompilerError
from magma.config import config, EnvConfig
from magma.logging import root_logger


config._register(circt_home=EnvConfig("CIRCT_HOME", None))

_logger = root_logger().getChild("mlir_backend")

_CIRCT_VERSION_RE_PATTERN = (
    r"^CIRCT "
    r"(?P<tag>.+)"  # usually circtorg-x.y.z but not relevant for us
    r"(?P<commits>\d+)-"
    r"g(?P<hash>[0-9A-Fa-f]+)"
)


class MlirToVerilogError(MlirCompilerError):
    pass


class BadCirctOptVersionStringError(MlirToVerilogError):
    pass


class UnsupportedCirctOptVersionError(MlirToVerilogError):
    pass


@dataclasses.dataclass
class MlirToVerilogOpts:
    split_verilog: bool = False
    check_circt_opt_version: bool = True


def _circt_home() -> Optional[pathlib.Path]:
    """Returns the CIRCT_HOME config if it is not None. Otherwise returns None.
    """
    if config.circt_home is None:
        return None
    return pathlib.Path(config.circt_home).resolve()


def _circt_opt_binary(circt_home: Optional[pathlib.Path]) -> str:
    """Returns the absolute path to the circt-opt binary if @circt_home is not
    None. Otherwise, returns just the binary name (i.e. looks for the binary in
    PATH).
    """
    if circt_home is not None:
        return str(circt_home / "build/bin/circt-opt")
    return "circt-opt"


def _circt_opt_cmd(
        circt_home: pathlib.Path,
        opts: MlirToVerilogOpts,
) -> List[str]:
    bin_ = f"{_circt_opt_binary(circt_home)}"
    export_verilog_pass = (
        "--export-split-verilog" if opts.split_verilog else "--export-verilog"
    )
    passes = [
        "--lower-seq-to-sv",
        "--canonicalize",
        "--hw-cleanup",
        "--prettify-verilog",
        export_verilog_pass,
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


def circt_opt_version() -> str:
    circt_home = _circt_home()
    circt_opt_binary = _circt_opt_binary(circt_home)
    ostream = io.TextIOWrapper(io.BytesIO())
    returncode = _run_subprocess(
        [circt_opt_binary, "--version"],
        stdin=io.BytesIO(),
        stdout=ostream.buffer,
    )
    ostream.seek(0)
    version = ostream.read()
    match = re.search(_CIRCT_VERSION_RE_PATTERN, version, re.MULTILINE)
    if match is None:
        raise BadCirctOptVersionStringError(version)
    return match["hash"]


def is_supported_circt_opt_version(version: str) -> bool:
    return version == "579d21b50"


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
    except (FileNotFoundError, PermissionError):
        return False
    return returncode == 0


def mlir_to_verilog(
        istream: io.RawIOBase,
        ostream: io.RawIOBase = sys.stdout,
        opts: MlirToVerilogOpts = MlirToVerilogOpts(),
):
    if opts.check_circt_opt_version:
        version = circt_opt_version()
        if not is_supported_circt_opt_version(version):
            raise UnsupportedCirctOptVersionError(version)
    circt_home = _circt_home()
    cmd = _circt_opt_cmd(circt_home, opts)
    _logger.debug(f"Running cmd: {' '.join(cmd)}")
    returncode = _run_subprocess(cmd, istream, ostream)
    if returncode != 0:
        cmd_str = " ".join(cmd)
        raise MlirToVerilogError(
            f"Error running {cmd_str}, got returncode {returncode}"
        )
