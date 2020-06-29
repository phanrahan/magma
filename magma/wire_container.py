from magma.logging import root_logger


_logger = root_logger()


class Wire:
    """
    Wire implements wiring.

    Each wire is represented by a bit.
    """
    def __init__(self, bit):
        self._bit = bit
        self._driving = []
        self._driver = None

    def __repr__(self):
        return repr(self._bit)

    def __str__(self):
        return str(self._bit)

    def anon(self):
        return self._bit.anon()

    def unwire(self, other):
        other._driving.remove(self)
        self._driver = None

    def connect(self, other, debug_info):
        """
        Connect two wires, self should be an input and other should be an
        output, or both should be inouts
        """
        if self._driver is not None:
            _logger.warning(
                "Wiring multiple outputs to same wire, using last connection."
                f" Input: {self._bit.debug_name}, "
                f" Old Output: {self._driver._bit.debug_name}, "
                f" New Output: {other._bit.debug_name}",
                debug_info=debug_info
            )
        if self._bit.is_output():
            _logger.error(f"Using `{self._bit.debug_name}` (an output) as an "
                          f"input", debug_info=debug_info)
            return
        if other._bit.is_input():
            _logger.error(f"Using `{other._bit.debug_name}` (an input) as an "
                          f"output", debug_info=debug_info)
            return
        if self._bit.is_inout() and not other._bit.is_inout():
            _logger.error(f"Using `{other._bit.debug_name}` (not inout) as an "
                          f"inout", debug_info=debug_info)
            return
        if not self._bit.is_inout() and other._bit.is_inout():
            _logger.error(f"Using `{self._bit.debug_name}` (not inout) as an "
                          f"inout", debug_info=debug_info)
            return

        self._driver = other
        other._driving.append(self)

    def trace(self, skip_self=True):
        """
        If a value is an input or an intermediate (undirected), trace it until
        there is an input or inout (this is the source)

        Upon the first invocation (from a user), we skip the current bit (so
        we don't trace to ourselves)
        """
        if self._driver is not None:
            return self._driver.trace(skip_self=False)
        if not skip_self and (self._bit.is_output() or self._bit.is_inout()):
            return self._bit
        return None

    def value(self):
        """
        Return the bit connected to this bit. Specifically, return the bit this
        bit is driving if it exists. Else if, there is a unique "drivee" bit,
        return that bit. Otherwise, return None.
        """
        if self._driver is not None:
            return self._driver._bit
        if len(self._driving) == 1:
            return self._driving[0]._bit
        return None

    def driven(self):
        return self.trace() is not None

    def wired(self):
        return self._driver or self._driving

    def driving(self):
        """
        Return a (possibly empty) list of all bits this bit is driving.
        """
        return [driving._bit for driving in self._driving]

    @property
    def driver(self):
        return self._driver

    @property
    def bit(self):
        return self._bit
