import functools

from .circuit import _definition_context_stack
from .display import Display


class Log(Display):
    level = None

    def __init__(self, display_str, args, file=None):
        display_prefix = type(self).__name__.upper()
        super().__init__(f"[{display_prefix}] {display_str}", args, file=file)

    def _make_cond_str(self, format_args):
        cond_str = super()._make_cond_str(format_args)
        level_check = f"`MAGMA_LOG_LEVEL <= {self.level}"
        if not cond_str:
            return level_check
        return f"({level_check}) && ({cond_str})"


class Debug(Log):
    level = 0


class Info(Log):
    level = 1


class Warning(Log):
    level = 2


class Error(Log):
    level = 3


def make_log_func(T):
    @functools.wraps(make_log_func)
    def log_func(log_str, *args, file=None):
        context = _definition_context_stack.peek()
        log = T(log_str, args, file=file)
        context.add_display(log)
        context.insert_default_log_level()
        return log
    return log_func


debug = make_log_func(Debug)
info = make_log_func(Info)
warning = make_log_func(Warning)
error = make_log_func(Error)
