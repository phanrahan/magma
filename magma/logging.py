import colorlog
import inspect
import io
import logging
import sys
import traceback
from .backend.util import make_relative
from .config import config, EnvConfig


config._register(
    log_stream=EnvConfig("MAGMA_LOG_STREAM", "stderr"),
    log_level=EnvConfig("MAGMA_LOG_LEVEL", "INFO"),
    include_traceback=EnvConfig("MAGMA_INCLUDE_WIRE_TRACEBACK", False, bool),
    traceback_limit=EnvConfig("MAGMA_ERROR_TRACEBACK_LIMIT", 5, int),
)


_staged_logging = False
_staged_logs = []


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


def _attach_traceback(msg, frame_selector, limit):
    """
    Attaches traceback string to @msg and returns new string.

    @frame_selector is a function which takes a list of stack frames and selects
    one. For example, it could select the frame based on an index, or based on
    the function names.
    """
    frame = frame_selector(inspect.stack()).frame
    with io.StringIO() as io_:
        traceback.print_stack(f=frame, limit=limit, file=io_)
        tb = io_.getvalue()
    msg = f"{msg}\n{tb}"
    return msg


def _frame_selector(frames):
    return frames[3]


def _get_additional_kwarg(kwargs, key):
    try:
        value = kwargs.pop(key)
        return value
    except KeyError:
        return None


class _MagmaLogger(logging.Logger):
    """
    Derivative of logging.Logger class, with two additional keyword args:
    * 'debug_info': Tuple of (file_name, line_no). If 'debug_info' is included,
       this source-level information is logged along with the message.
    * 'include_traceback': If True, a traceback is printed along with the
       message.
    """
    @staticmethod
    def __with_preamble(fn, msg, *args, **kwargs):
        debug_info = _get_additional_kwarg(kwargs, "debug_info")
        if debug_info:
            msg = _attach_debug_info(msg, debug_info)
        include_traceback = _get_additional_kwarg(kwargs, "include_traceback")
        if include_traceback or config.include_traceback:
            msg = _attach_traceback(
                msg, _frame_selector, config.traceback_limit)
        fn(msg, *args, **kwargs)

    def log(self, level, msg, *args, **kwargs):
        key = logging.getLevelName(level).lower()
        fn = getattr(_MagmaLogger, key)
        fn(self, msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        global _staged_logging
        if _staged_logging:
            _staged_logs.append((self, logging.DEBUG, msg, args, kwargs))
            return
        _MagmaLogger.__with_preamble(super().debug, msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        global _staged_logging
        if _staged_logging:
            _staged_logs.append((self, logging.INFO, msg, args, kwargs))
            return
        _MagmaLogger.__with_preamble(super().info, msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        global _staged_logging
        if _staged_logging:
            _staged_logs.append((self, logging.WARNING, msg, args, kwargs))
            return
        _MagmaLogger.__with_preamble(super().warning, msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        global _staged_logging
        if _staged_logging:
            _staged_logs.append((self, logging.ERROR, msg, args, kwargs))
            return
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


def flush():
    global _staged_logs
    for logger, level, obj, args, kwargs in _staged_logs:
        logger.log(level, obj, *args, **kwargs)
    _staged_logs = []


def root_logger():
    return logging.getLogger("magma")


def stage_logger():
    global _staged_logging
    _staged_logging = True


def unstage_logger():
    global _staged_logging
    _staged_logging = False
    flush()
