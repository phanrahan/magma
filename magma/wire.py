import magma as m
from .compatibility import IntegerTypes
from .debug import debug_wire
from .logging import root_logger
from .t import MagmaProtocol


_logger = root_logger()


@debug_wire
def wire(o, i, debug_info=None):
    if isinstance(o, MagmaProtocol):
        o = o._get_magma_value_()
    if isinstance(i, MagmaProtocol):
        i = i._get_magma_value_()

    # Wire(o, Circuit).
    if hasattr(i, 'interface'):
        i.wire(o, debug_info)
        return

    # Replace output Circuit with its output (should only be 1 output).
    if hasattr(o, 'interface'):
        # If wiring a Circuit to a Port then circuit should have 1 output.
        o_orig = o
        o = o.interface.outputs()
        if len(o) != 1:
            _logger.error(f"Can only wire circuits with one output. Argument "
                          f"0 to wire `{o_orig.debug_name}` has outputs {o}",
                          debug_info=debug_info)
            return
        o = o[0]

    # If o is an input.
    if not isinstance(o, IntegerTypes) and o.is_input():
        # If i is not an input.
        if isinstance(i, IntegerTypes) or not i.is_input():
            # Flip i and o.
            i, o = o, i

    # Wire(o, Type).
    i.wire(o, debug_info)


class Wire:
    """
    Wire implement wiring.

    Each wire is represented by a Bit().
    """
    def __init__(self, bit):
        self.bit = bit
        self.driving = []
        self.driver = None

    def __repr__(self):
        return repr(self.bit)

    def __str__(self):
        return str(self.bit)

    def anon(self):
        return self.bit.anon()

    def unwire(self, other):
        other.driving.remove(self)
        self.driver = None

    def connect(self, other, debug_info):
        """
        Connect two wires, self should be an input and other should be an
        output, or both should be inouts
        """
        if self.driver is not None and self.bit.is_input():
            _logger.warning(
                "Wiring multiple outputs to same wire, using last connection."
                f" Input: {self.bit.debug_name}, "
                f" Old Output: {self.driver.bit.debug_name}, "
                f" New Output: {other.bit.debug_name}",
                debug_info=debug_info
            )
        if self.bit.is_output():
            _logger.error(f"Using `{self.bit.debug_name}` (an output) as an "
                          f"input", debug_info=debug_info)
            return
        if other.bit.is_input():
            _logger.error(f"Using `{other.bit.debug_name}` (an input) as an "
                          f"output", debug_info=debug_info)
            return
        if self.bit.is_inout() and not other.bit.is_inout():
            _logger.error(f"Using `{other.bit.debug_name}` (not inout) as an "
                          f"inout", debug_info=debug_info)
            return
        if not self.bit.is_inout() and other.bit.is_inout():
            _logger.error(f"Using `{self.bit.debug_name}` (not inout) as an "
                          f"inout", debug_info=debug_info)
            return

        self.driver = other
        other.driving.append(self)

    def trace(self, skip_self=True):
        """
        If a value is an input or an intermediate (undirected), trace it until
        there is an input or inout (this is the source)

        Upon the first invocation (from a user), we skip the current bit (so
        we don't trace to ourselves)
        """
        if self.driver is not None:
            return self.driver.trace(skip_self=False)
        if not skip_self and (self.bit.is_output() or self.bit.is_inout()):
            return self.bit
        return None

    def value(self):
        """
        Return the driver of this wire
        """
        if self.bit.is_output():
            raise TypeError("Can only get value of non outputs")
        if self.driver is None:
            return None
        return self.driver.bit

    def driven(self):
        return self.trace() is not None

    def wired(self):
        return self.driver or self.driving
