from magma.logging import root_logger


_logger = root_logger()


class Wire:
    """
    Wire implements wiring.

    Each wire is represented by a bit.
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
        if self.driver is not None:
            return self.driver.bit
        if len(self.driving) == 1:
            return self.driving[0].bit
        return None

    def driven(self):
        return self.trace() is not None

    def wired(self):
        return self.driver or self.driving
