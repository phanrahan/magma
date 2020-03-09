from .verilog_utils import value_to_verilog_name
from .t import Type
from .view import PortView


def inline_verilog(format_str, **kwargs):
    # Return staged format because we cannot do until the circuit io has been
    # realized (during defn it is anonymous)
    # Return tuple so you can += multiple inline strings
    return ((format_str, kwargs), )
