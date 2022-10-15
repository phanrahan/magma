import abc
import functools
import logging as py_logging

from magma.config import config, EnvConfig
from magma.debug import debug_wire, debug_unwire
from magma.logging import root_logger, StagedLogRecord
from magma.when import (
    get_curr_block as get_curr_when_block,
    no_when,
    temp_when
)


config._register(
    rewire_log_level=EnvConfig("MAGMA_REWIRE_LOG_LEVEL", "WARNING")
)


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
            # TODO(rsetaluri): Issue a different warning in the case of the old
            # driver being a "conditional" driver (i.e. from a when context).
            old_driver = self._driver
            self.unwire(old_driver)
            _logger.log(
                py_logging.getLevelName(config.rewire_log_level),
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
        if (
            not skip_self and self._bit.has_children() and self._bit.driven()
        ):
            # Driven non-bulk, so trace children
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
        """
        * _enclosing_when_context: The when context active when this object was
                                   created.  Lazily created child objects
                                   should inherit their parent's
                                   enclosing when context using the
                                   `set_enclosing_when_context` API.
        * _wired_when_contexts: A list of when contexts in which this object
                                was conditionally wired.  Used to track the
                                contexts that should be updated when unwiring.
        """
        self._wire = Wire(self)
        self._enclosing_when_context = get_curr_when_block()
        self._wired_when_contexts = []

    def set_enclosing_when_context(self, ctx):
        self._enclosing_when_context = ctx

    @property
    def enclosing_when_context(self):
        return self._enclosing_when_context

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

    def _remove_from_wired_when_contexts(self):
        for ctx in self._wired_when_contexts:
            ctx.remove_conditional_wire(self)
        self._wired_when_contexts = []

    @debug_unwire
    def unwire(self, o=None, debug_info=None, keep_wired_when_contexts=False):
        if o is not None:
            o = o._wire
        self._wire.unwire(o, debug_info)
        if not keep_wired_when_contexts:
            self._remove_from_wired_when_contexts()

    def _wire_impl(self, o, debug_info):
        self._wire.connect(o._wire, debug_info)
        self.debug_info = debug_info
        o.debug_info = debug_info

    def wire(self, o, debug_info):
        curr_when_block = get_curr_when_block()
        is_conditional = (
            curr_when_block is not None
            and curr_when_block is not self._enclosing_when_context
        )
        if not is_conditional:
            self._wire_impl(o, debug_info)
            return
        curr_when_block.add_conditional_wire(self, o)
        self._wired_when_contexts.append(curr_when_block)

    @debug_wire
    def rewire(self, o, debug_info=None):
        self.unwire(debug_info=debug_info)
        self.wire(o, debug_info=debug_info)


class AggregateWireable(Wireable):
    def __init__(self):
        super().__init__()
        # Flag used to mark a value that is currently being
        # resolved, and therefor it doesn't need to repeat the
        # resolution logic that is being done in the calling code
        self._should_resolve = True

    @abc.abstractmethod
    def has_elaborated_children(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def _enumerate_children(self):
        raise NotImplementedError()

    def _get_conditional_drivee_info(self):
        """
        * wired_when_contexts: list of contexts in which this value appears as
                               conditionally driven.

        * conditional_wires: for each ctx in `wired_when_contexts`, contains a
                             list of conditional wire objects where `self` is a
                             drivee.

        * default_drivers: for each ctx in `wired_when_contexts`, contains the
                           default driver (if it exists) for `self`.
        """
        conditional_wires = []
        default_drivers = []
        for ctx in self._wired_when_contexts:
            conditional_wires.append(ctx.get_conditional_wires_for_drivee(self))
            default_drivers.append(ctx._default_drivers.pop(self, None))
        return self._wired_when_contexts, conditional_wires, default_drivers

    def _rewire_conditional_children(self, wired_when_contexts,
                                     conditional_wires, default_drivers):
        for i, child in self._enumerate_children():
            for ctx, wires, default_driver in zip(wired_when_contexts,
                                                  conditional_wires,
                                                  default_drivers):
                if default_driver:
                    # Default driver is wired outside of a when context.
                    with no_when():
                        child.wire(default_driver[i])

                # Use original wired when context.
                with temp_when(ctx):
                    for wire in wires:
                        child.wire(wire.driver[i])

    def _resolve_conditional_children(self, value):
        # Save conditional wire info before unwire happens
        info = self._get_conditional_drivee_info()

        AggregateWireable.unwire(self, value)

        self._rewire_conditional_children(*info)

    def _resolve_driven_bulk_wire(self):
        # Remove bulk wire since children will now track the wiring
        value = self._wire.value()

        if self._wired_when_contexts:
            return self._resolve_conditional_children(value)

        # Else, was not wired in a when context, so children should not be
        # wired in a when context
        with no_when():
            AggregateWireable.unwire(self, value)

            for i, child in self._enumerate_children():
                child.wire(value[i])

    def _resolve_bulk_wire(self):
        """
        If a child reference is made, we "expand" a bulk wire into the
        constiuent children to maintain consistency
        """
        if not self._should_resolve:
            return
        # Trace as far back as possible to know where to start
        source = self._wire.trace()
        if source is None:
            source = self
        source._should_resolve = False

        # Process values one at a time so that we avoid recursion
        # error for large wire chains
        to_process = source._wire.driving()
        while to_process:
            next = to_process.pop()
            next._should_resolve = False
            next._resolve_driven_bulk_wire()
            to_process.extend(next._wire.driving())


def aggregate_wireable_method(fn):

    @functools.wraps(fn)
    def wrapper(self, *args, **kwargs):
        if self.has_elaborated_children():
            return fn(self, *args, **kwargs)
        wireable_fn = getattr(AggregateWireable, fn.__name__)
        return wireable_fn(self, *args, **kwargs)

    return wrapper
