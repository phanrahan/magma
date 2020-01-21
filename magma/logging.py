import colorlog
import logging
import sys
from .backend.util import make_relative
from .config import config, EnvConfig


config._register(
    log_stream=EnvConfig("MAGMA_LOG_STREAM", "stderr"),
    log_level=EnvConfig("MAGMA_LOG_LEVEL", "INFO"),
    include_wire_traceback=EnvConfig("MAGMA_INCLUDE_WIRE_TRACEBACK", False),
    error_traceback_limit=EnvConfig("MAGMA_ERROR_TRACEBACK_LIMIT", "5"),
)


def _make_bold(string):
    return f"\033[1m{string}\033[0m"


def _get_source_line(filename, lineno):
    with open(filename, "r") as f:
        return f.readlines()[lineno - 1]


def _attach_debug_info(msg, debug_info):
    file = debug_info[0]
    line = debug_info[1]
    line_info = _make_bold(f"{make_relative(file)}:{line}")
    msg = f"{line_info}: {msg}"
    try:
        source = _get_source_line(file, line).rstrip("\n")
        source = f">> {source}"
    except FileNotFoundError:
        source = f"(Could not file file {file})"
    msg = f"{msg}\n{source}"
    return msg


_MISSING = object()


class _MagmaLogger(logging.Logger):
    @staticmethod
    def __with_preamble(fn, msg, *args, **kwargs):
        debug_info = kwargs.get("debug_info", _MISSING)
        if debug_info is not _MISSING:
            if debug_info:
                msg = _attach_debug_info(msg, debug_info)
            kwargs.pop("debug_info")
        fn(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        _MagmaLogger.__with_preamble(super().debug, msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        _MagmaLogger.__with_preamble(super().info, msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        _MagmaLogger.__with_preamble(super().warning, msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        _MagmaLogger.__with_preamble(super().error, msg, *args, **kwargs)


# Set logging class to _MagmaLogger to override logging behavior. Also, setup
# root logger parameters.
logging.setLoggerClass(_MagmaLogger)
_log_stream = getattr(sys, config.log_stream)
_root_logger = logging.getLogger("magma")
_handler = colorlog.StreamHandler(_log_stream)
_handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(levelname)s%(reset)s:%(name)s:%(message)s'))
_root_logger.addHandler(_handler)
_root_logger.setLevel(config.log_level)


def root_logger():
    return logging.getLogger("magma")
