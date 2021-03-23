from magma.logging import root_logger


_logger = root_logger()


class WiringLog:
    def __init__(self, tpl, *bits):
        self.tpl = tpl
        self.bits = bits

    def get_debug_name(self, bit):
        if isinstance(bit, int):
            return bit
        return bit.debug_name

    def __str__(self):
        bits = [self.get_debug_name(bit) for bit in self.bits]
        return self.tpl.format(*bits)


class Wire:
    """
    Wire implements wiring.

    Each wire is represented by a bit.
    """
    def __init__(self, value):
        self._val = value
        self._driving = []
        self._driver = None

    def __repr__(self):
        return repr(self._val)

    def __str__(self):
        return str(self._val)

    def anon(self):
        return self._val.anon()

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
                WiringLog(
                    ("Wiring multiple outputs to same wire, using last "
                     "connection. Input: {}, Old Output: {}, New Output: {}"),
                    self._val, self._driver.val, other.val),
                debug_info=debug_info
            )
        if self._val.is_output():
            _logger.error(
                WiringLog("Using `{}` (an output) as an input", self._val),
                debug_info=debug_info
            )
            return
        if other.val.is_input():
            _logger.error(
                WiringLog("Using `{}` (an input) as an output", other.val),
                debug_info=debug_info
            )
            return
        if self._val.is_inout() and not other.val.is_inout():
            _logger.error(
                WiringLog("Using `{}` (not inout) as an inout", other.val),
                debug_info=debug_info
            )
            return
        if not self._val.is_inout() and other.val.is_inout():
            _logger.error(
                WiringLog("Using `{}` (not inout) as an inout", self._val),
                debug_info=debug_info
            )
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
            return self._driver.val.trace(skip_self=False)
        if not skip_self and (self._val.is_output() or self._val.is_inout()):
            return self._val
        return None

    def value(self):
        """
        Return the bit connected to this bit. Specifically, return the bit this
        bit is driving if it exists. Else if, there is a unique "drivee" bit,
        return that bit. Otherwise, return None.
        """
        if self._driver is not None:
            return self._driver.val
        if len(self._driving) == 1:
            return self._driving[0].val
        return None

    def driven(self):
        return self._driver is not None

    def wired(self):
        return self._driver or self._driving

    def driving(self):
        """
        Return a (possibly empty) list of all bits this bit is driving.
        """
        return [driving.val for driving in self._driving]

    @property
    def driver(self):
        return self._driver

    @property
    def val(self):
        # TODO: This name is a bit confusing with `value` which is around for
        # legacy reasons, perhaps we can rename value instead of renaming this
        # (e.g. using driver/drivee instead of value)
        # We are using `val` to generalize `bit` since wires can now refer to
        # other types (for tracking bulk connections)
        return self._val
