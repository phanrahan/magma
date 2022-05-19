from magma.logging import root_logger, StagedLogRecord
from magma.when import safe_peek_defn_when_cond_stack


_logger = root_logger()


class WiringLogRecord(StagedLogRecord):
    def __init__(self, tpl: str, *values):
        super().__init__(tpl)
        self._values = values

    @staticmethod
    def _get_debug_name(value):
        if isinstance(value, int):
            return value
        return value.debug_name

    def args(self):
        return [
            WiringLogRecord._get_debug_name(value) for value in self._values
        ]


# TODO(rsetaluri): Remove this alias.
WiringLog = WiringLogRecord


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

    def unwire(self, other=None, debug_info=None):
        if other is None:
            if self._driver is None:
                _logger.warning(
                    WiringLog("Unwire called on undriven value {}, ignoring",
                              self._bit),
                    debug_info=debug_info
                )
                return
            other = self._driver
        other._driving.remove(self)
        self._driver = None

    def connect(self, other, debug_info):
        """
        Connect two wires, self should be an input and other should be an
        output, or both should be inouts
        """
        if self._driver is not None:
            old_driver = self._driver
            self.unwire(old_driver)
            _logger.warning(
                WiringLog(
                    ("Wiring multiple outputs to same wire, using last "
                     "connection. Input: {}, Old Output: {}, New Output: {}"),
                    self._bit, old_driver._bit, other._bit),
                debug_info=debug_info
            )
        if self._bit.is_output():
            _logger.error(
                WiringLog("Using `{}` (an output) as an input", self._bit),
                debug_info=debug_info
            )
            return
        if other._bit.is_input():
            _logger.error(
                WiringLog("Using `{}` (an input) as an output", other._bit),
                debug_info=debug_info
            )
            return
        if self._bit.is_inout() and not other._bit.is_inout():
            _logger.error(
                WiringLog("Using `{}` (not inout) as an inout", other._bit),
                debug_info=debug_info
            )
            return
        if not self._bit.is_inout() and other._bit.is_inout():
            _logger.error(
                WiringLog("Using `{}` (not inout) as an inout", self._bit),
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
            return self._driver.trace(skip_self=False)
        if not skip_self and (self._bit.is_output() or self._bit.is_inout()):
            return self._bit
        if not skip_self and self._bit.has_children():
            # Could be an Array driven non-bulk, so check if children can be
            # traced
            return self._bit.trace(skip_self=False)
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
        return self._driver is not None

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


class Wireable:
    def __init__(self):
        self._wire = Wire(self)
        self._conditional_drivers = {}

    def wired(self):
        return self._wire.wired()

    # return the input or output Bit connected to this Bit
    def trace(self, skip_self=True):
        return self._wire.trace(skip_self)

    # return the output Bit connected to this input Bit
    def value(self):
        return self._wire.value()

    def driven(self):
        return self._wire.driven()

    def driving(self):
        return self._wire.driving()

    def unwire(i, o=None, debug_info=None):
        if o is not None:
            o = o._wire
        i._wire.unwire(o, debug_info)

    def _conditional_wire(self, o, debug_info):
        if self.driven():
            value = self.value()
            self._conditional_drivers[None] = value
            self.unwire(value)
        # TODO(when): Add debug_info
        when_cond_stack = peek_defn_when_cond_stack()
        self._conditional_drivers[tuple(when_cond_stack)] = o
        when_cond_stack.peek().add_conditional_wire(self, o)

    def _unconditional_wire(self, o, debug_info):
        if self._conditional_drivers:
            # If we drive a value outside of a when, but it already has
            # conditional drivers, we clear them because we now have a
            # "new" driver
            # TODO(when): Add warning here
            for cond in self._conditional_drivers:
                if cond is None:
                    continue
                cond[-1].remove_conditional_wire(self)
            self._conditional_drivers = {}
        self._wire.connect(o._wire, debug_info)
        self.debug_info = debug_info
        o.debug_info = debug_info

    def wire(self, o, debug_info):
        # NOTE: We use safe peek here because there are existing wiring tests
        # that don't happen inside a circuit context
        if safe_peek_defn_when_cond_stack():
            self._conditional_wire(o, debug_info)
        else:
            self._unconditional_wire(o, debug_info)
