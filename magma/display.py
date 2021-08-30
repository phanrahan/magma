from .circuit import _definition_context_stack
from .t import Type


class _Time:
    pass


def time():
    return _Time()


class _Event:
    def __init__(self, value):
        if not isinstance(value, Type):
            raise TypeError("Expected magma value for event")
        self.value = value


class _Posedge(_Event):
    verilog_str = "posedge"


class _Negedge(_Event):
    verilog_str = "negedge"


def posedge(value):
    return _Posedge(value)


def negedge(value):
    return _Negedge(value)


def _make_display_format_arg(value, format_args):
    # Unique name based on object id
    var = f"_display_var_{id(value)}"
    if isinstance(value, _Time):
        # Insert $time string
        value = "$time"
    # Insert into a format kwargs map
    format_args[var] = value
    # Wrap in format braces so it is replaced later on
    var = f"{{{var}}}"
    return var


class Display:
    def __init__(self, display_str, args, file):
        # Encode to handle newlines, etc... properly
        self.display_str = display_str.encode('unicode_escape').decode()
        self.args = args
        self.events = []
        self.cond = None
        self.file = file

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
        if not isinstance(event, (Type, _Event)):
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
                if isinstance(event, _Event):
                    value = value.value
                var = _make_display_format_arg(value, format_args)
                # prepend event if not just plain signal
                if isinstance(event, _Event):
                    var = f"{event.verilog_str} {var}"
                event_strs.append(var)
            event_str = ", ".join(event_strs)

        cond_str = self._make_cond_str(format_args)
        if cond_str:
            cond_str = f"if ({cond_str}) "

        display_str = f"$display("
        if self.file is not None:
            display_str = f"$fdisplay(\\_file_{self.file.filename} , "  # noqa
        format_str = f"""\
always @({event_str}) begin
    {cond_str}{display_str}\"{self.display_str}\"{display_args_str});
end
"""
        return format_str, format_args, {}


def display(display_str, *args, file=None):
    context = _definition_context_stack.peek()
    disp = Display(display_str, args, file)
    context.add_display(disp)
    return disp


class File:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode

        context = _definition_context_stack.peek()
        context.add_file(self)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass
