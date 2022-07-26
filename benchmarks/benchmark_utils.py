import platform
import subprocess
import timeit
from typing import Callable


def get_platform() -> str:
    return platform.platform()


def get_processor_info() -> str:
    system = platform.system()
    if system == "Windows":
        return platform.processor()
    if system == "Darwin":
        return subprocess.check_output([
            "/usr/sbin/sysctl", "-n", "machdep.cpu.brand_string"
        ]).decode("ascii").strip()
    if system == "Linux":
        command = "cat /proc/cpuinfo"
        return subprocess.check_output(
            command, shell=True
        ).decode("ascii").strip()
    raise SystemError(f"Unknown system: {system}")


def get_git_commit() -> str:
    return subprocess.check_output([
        "git", "rev-parse", "--short", "HEAD"
    ]).decode("ascii").strip()


def get_average_time(fn: Callable, num_runs: int) -> float:
    return timeit.Timer(fn).timeit(number=num_runs) / float(num_runs)
