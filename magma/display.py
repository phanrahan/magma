from .circuit import _definition_context_stack
from .t import Type


class Event:
    def __init__(self, value):
        if not isinstance(value, Type):
            raise TypeError("Expected magma value for event")
        self.value = value


class Posedge(Event):
    verilog_str = "posedge"


class Negedge(Event):
    verilog_str = "negedge"


def posedge(value):
    return Posedge(value)


def negedge(value):
    return Negedge(value)


def _make_display_format_arg(value, format_args):
    # Unique name based on object id
    var = f"_display_var_{id(value)}"
    # Insert into a format kwargs map
    format_args[var] = value
    # Wrap in format braces so it is replaced later on
    var = f"{{{var}}}"
    return var


class Display:
    def __init__(self, display_str, args):
        # Encode to handle newlines, etc... properly
        self.display_str = display_str.encode('unicode_escape').decode()
        self.args = args
        self.events = []
        self.cond = None

    def if_(self, cond):
        """
        Method to set condition for display

            # Display if CE (enable) is high
            m.display("x=%d", x).when(m.posedge(io.CLK))\
                                .if_(io.CE)

        """
        if self.cond is not None:
            raise Exception("Can only invoke if_ once on display")
        self.cond = cond
        return self

    def when(self, event):
        """
        Allows chaining to set event for display, e.g.

            m.display("x=%d", x).when(m.posedge(io.CLK))\
                                .when(m.negedge(io.ASYNCRESET))

        """
        if not isinstance(event, (Type, Event)):
            raise TypeError("Expected magma value or event for when argument")
        self.events.append(event)
        return self

    def _make_cond_str(self, format_args):
        if self.cond is not None:
            return _make_display_format_arg(self.cond, format_args)
        return ""

    def get_inline_verilog(self):
        format_args = {}
        display_args = []
        # arguments to the dipslay function are unique names that are
        # interpolated later by the inline_verilog syntax
        #     e.g. $display("...", {_display_var_0}, {_display_var_1});
        for arg in self.args:
            display_args.append(_make_display_format_arg(arg, format_args))

        display_args_str = ""
        if display_args:
            display_args_str = ", " + ", ".join(display_args)

        # Default all events
        event_str = "*"
        if self.events:
            event_strs = []
            for event in self.events:
                value = event
                # Could be sensitive to plain signal
                if isinstance(event, Event):
                    value = value.value
                var = _make_display_format_arg(value, format_args)
                # prepend event if not just plain signal
                if isinstance(event, Event):
                    var = f"{event.verilog_str} {var}"
                event_strs.append(var)
            event_str = ", ".join(event_strs)

        cond_str = self._make_cond_str(format_args)
        if cond_str:
            cond_str = f"if ({cond_str}) "

        format_str = f"""\
always @({event_str}) begin
    {cond_str}$display(\"{self.display_str}\"{display_args_str});
end
"""
        return format_str, format_args, {}


def display(display_str, *args):
    context = _definition_context_stack.peek()
    disp = Display(display_str, args)
    context.add_display(disp)
    return disp
