import abc
import colorlog
import contextlib
import inspect
import io
import logging
import sys
import traceback

from magma.backend.util import make_relative
from magma.common import Stack
from magma.config import config, EnvConfig


config._register(
    log_stream=EnvConfig("MAGMA_LOG_STREAM", "stderr"),
    log_level=EnvConfig("MAGMA_LOG_LEVEL", "INFO"),
    include_traceback=EnvConfig("MAGMA_INCLUDE_WIRE_TRACEBACK", False, bool),
    traceback_limit=EnvConfig("MAGMA_ERROR_TRACEBACK_LIMIT", 5, int),
)


_staged_logs_stack = Stack()
_log_capturer_stack = Stack()


def _make_bold(string):
    return f"\033[1m{string}\033[0m"


def _get_source_line(filename, lineno):
    with open(filename, "r") as f:
        return f.readlines()[lineno - 1]


def _attach_debug_info(msg, debug_info):
    file = debug_info.filename
    line = debug_info.lineno
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


def get_staged_logs_stack() -> Stack:
    global _staged_logs_stack
    return _staged_logs_stack


class _MagmaLogger(logging.Logger):
    """
    Derivative of logging.Logger class, with two additional keyword args:
    * 'debug_info': Tuple of (file_name, line_no). If 'debug_info' is included,
       this source-level information is logged along with the message.
    * 'include_traceback': If True, a traceback is printed along with the
       message.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._raw = False

    @property
    def raw(self) -> bool:
        return self._raw

    @raw.setter
    def raw(self, raw: bool):
        self._raw = raw

    @contextlib.contextmanager
    def as_raw(self):
        prev_raw = self.raw
        self.raw = True
        try:
            yield self
        finally:
            self.raw = prev_raw

    def _log(self, level, msg, args, **kwargs):
        if not self.raw and self._staged_log(level, msg, args, **kwargs):
            return
        self._raw_log(level, msg, args, **kwargs)

    def _staged_log(self, level, msg, args, **kwargs) -> bool:
        staged_logs_stack = get_staged_logs_stack()
        try:
            staged_logs = staged_logs_stack.peek()
        except IndexError:
            return False
        staged_logs.append((self, level, msg, args, kwargs))
        return True

    def _capture_log(self, level, msg, args, **kwargs):
        try:
            log_capturer = get_log_capturer()
        except IndexError:
            return
        log_capturer.add_log((level, msg, args, kwargs))

    def _raw_log(self, level, msg, args, **kwargs):
        debug_info = _get_additional_kwarg(kwargs, "debug_info")
        if debug_info:
            msg = _attach_debug_info(msg, debug_info)
        include_traceback = _get_additional_kwarg(kwargs, "include_traceback")
        if include_traceback or config.include_traceback:
            msg = _attach_traceback(
                msg, _frame_selector, config.traceback_limit)
        self._capture_log(level, msg, args, **kwargs)
        super()._log(level, msg, args, **kwargs)


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


# NOTE(rsetaluri): For some reason the following code which uses
# contextlib.contextmanager results in the context manager being entered into
# twice. It may be cached somewhere in the pipeline.
#
#    @contextlib.contextmanager
#    def logging_level(level):
#        root = root_logger()
#        prev_level = root.level
#        root.setLevel(level)
#        try:
#            yield
#        finally:
#            root.setLevel(prev_level)
class logging_level:
    def __init__(self, level):
        self.level = level
        self.root = root_logger()

    def __enter__(self):
        self.prev_level = self.root.level
        self.root.setLevel(self.level)

    def __exit__(self, *_):
        self.root.setLevel(self.prev_level)


def stage_logger():
    get_staged_logs_stack().push([])


def _flush(staged_logs):
    for logger, level, obj, args, kwargs in staged_logs:
        with logger.as_raw():
            logger.log(level, obj, *args, **kwargs)


def flush():
    staged_logs = get_staged_logs_stack().pop()
    _flush(staged_logs)
    return staged_logs


def unstage_logger():
    return flush()


def flush_all():
    staged_logs_stack = get_staged_logs_stack()
    while staged_logs_stack:
        staged_logs = staged_logs_stack.pop()
        _flush(staged_logs)


@contextlib.contextmanager
def staged_logs():
    stage_logger()
    staged_logs = get_staged_logs_stack().peek()
    try:
        yield staged_logs
    finally:
        unstage_logger()


class StagedLogRecord(abc.ABC):
    def __init__(self, tpl: str):
        self._tpl = tpl

    @abc.abstractmethod
    def args(self):
        raise NotImplementedError()

    def __str__(self):
        return self._tpl.format(*self.args())


def _get_log_capturer_stack() -> Stack:
    global _log_capturer_stack
    return _log_capturer_stack


def push_log_capturer(log_capturer):
    _get_log_capturer_stack().push(log_capturer)


def pop_log_capturer():
    _get_log_capturer_stack().pop()


def get_log_capturer():
    return _get_log_capturer_stack().peek()


@contextlib.contextmanager
def capture_logs(log_capturer):
    push_log_capturer(log_capturer)
    try:
        yield
    finally:
        pop_log_capturer()
