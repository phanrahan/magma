import argparse
import contextlib
import logging
import os
import pathlib
import string
import sys
import subprocess
import tempfile


_YOSYS_BINARY_ENV_KEY = "YOSYS_BINARY"
_YOSYS_BINARY_DEFAULT = "yosys"

_YOSYS_CHECK_EQUIV_TPL = """
    read_verilog $file1
    rename $top top1
    proc
    memory
    flatten top1
    hierarchy -top top1

    read_verilog $file2
    rename $top top2
    proc
    memory
    flatten top2
    # hierarchy -top top2

    clean -purge
    opt -purge
    equiv_make top1 top2 equiv
    hierarchy -top equiv
    equiv_simple -undef
    equiv_induct -undef
    equiv_status -assert
"""

_SV2V_BINARY_ENV_KEY = "SV2V_BINARY"
_SV2V_BINARY_DEFAULT = "sv2v"


def _temporary_directory(
        delete: bool = False,
        *args, **kwargs
) -> contextlib.AbstractContextManager:
    if delete:
        return tempfile.TemporaryDirectory(*args, **kwargs)
    path = pathlib.Path("./.check-equiv")
    path.mkdir(exist_ok=True)
    return contextlib.nullcontext(enter_result=str(path))


def _get_sv2v_binary() -> str:
    return os.getenv(_SV2V_BINARY_ENV_KEY) or _SV2V_BINARY_DEFAULT


@contextlib.contextmanager
def _sv2v_impl(file: str) -> contextlib.AbstractContextManager:
    with _temporary_directory() as temp_dir:
        outfile = f"{temp_dir}/{pathlib.Path(file).name}"
        args = [_get_sv2v_binary(), file]
        args += ["-w", outfile]
        logging.info(f"Running {' '.join(map(str, args))}")
        proc = subprocess.Popen(args)
        proc.wait()
        try:
            yield outfile
        finally:
            pass


@contextlib.contextmanager
def _sv2v(*files) -> contextlib.AbstractContextManager:
    outfiles = []
    with contextlib.ExitStack() as stack:
        outfiles = tuple(stack.enter_context(_sv2v_impl(file)) for file in files)
        try:
            yield outfiles
        finally:
            pass


def _maybe_sv2v(sv2v: bool, *files) -> contextlib.AbstractContextManager:
    if not sv2v:
        return contextlib.nullcontext(enter_result=files)
    return _sv2v(*files)


def _get_yosys_binary() -> str:
    return os.getenv(_YOSYS_BINARY_ENV_KEY) or _YOSYS_BINARY_DEFAULT


def _run_yosys(file1: str, file2: str, top: str) -> subprocess.Popen:
    logging.info(
        f"Checking equivalence between {file1} and {file2} "
        f"(top={top})"
    )
    tpl = string.Template(_YOSYS_CHECK_EQUIV_TPL)
    script = tpl.substitute(file1=file1, file2=file2, top=top)
    logging.info(f"Running yosys script: {script}")
    args = [_get_yosys_binary()]
    proc = subprocess.Popen(
        args,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    proc.stdin.write(script.encode())
    proc.stdin.close()
    proc.wait()
    return proc


def _handle_result(proc: subprocess.Popen):
    stdout = proc.stdout.read().decode()
    stdout += proc.stderr.read().decode()
    has_error = (
        proc.returncode
        or "ERROR" in stdout
    )
    if not has_error:
        sys.stdout.write("PASS\n")
        return
    sys.stderr.write(stdout)
    sys.stdout.write("FAIL\n")


def _main() -> int:
    parser = argparse.ArgumentParser(
        description="Check equivalence of two (verilog) circuits",
    )
    parser.add_argument("file1", type=str)
    parser.add_argument("file2", type=str)
    parser.add_argument("top", type=str)
    parser.add_argument('--sv2v', action="store_true", default=False)
    parser.add_argument(
        '-v', '--verbose',
        action="store_const", dest="loglevel", const=logging.INFO,
    )
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)
    with _maybe_sv2v(args.sv2v, *(args.file1, args.file2)) as (file1, file2):
        proc = _run_yosys(file1, file2, args.top)
    _handle_result(proc)
    return proc.returncode


if __name__ == "__main__":
    exit(_main())
