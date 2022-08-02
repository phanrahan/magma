from typing import Union
from magma.bit import Bit
from magma.logging import root_logger
from magma.primitives.mux import mux
from magma.t import Type, In, Out, Direction
from magma.protocol_type import MagmaProtocol
from magma.tuple import Product, ProductKind


_logger = root_logger()


class ReadyValidException(Exception):
    pass


def _check_T(cls, T):
    if not issubclass(T, (Type, MagmaProtocol)):
        raise TypeError(
            f"{cls}[T] expected T to be a subclass of m.Type or"
            f" m.MagmaProtocol not {T}"
        )
    undirected_T = T.undirected_t
    if undirected_T is not T:
        _logger.warning(
            f"Type {T} used with ReadyValid is not undirected, converting"
            " to undirected type"
        )
    return undirected_T


def _maybe_add_data(cls, fields, T, qualifier):
    if T is None:
        return
    T = _check_T(cls, T)
    fields["data"] = qualifier(T)


class HandShakeError(Exception):
    pass


class EnqError(HandShakeError):
    def __init__(self, cls):
        super().__init__(f"{cls} does not support enq")


class NoEnqError(HandShakeError):
    def __init__(self, cls):
        super().__init__(f"{cls} does not support no_enq")


class DeqError(HandShakeError):
    def __init__(self, cls):
        super().__init__(f"{cls} does not support deq")


class NoDeqError(HandShakeError):
    def __init__(self, cls):
        super().__init__(f"{cls} does not support no_deq")


def _enq_error(self, value, when=True):
    raise EnqError(type(self))


def _no_enq_error(self, value, when=True):
    raise NoEnqError(type(self))


def _deq_error(self, value, when=True):
    raise DeqError(type(self))


def _no_deq_error(self, value, when=True):
    raise NoDeqError(type(self))


class HandShakeKind(ProductKind):
    """Undirected handshake type."""
    _qualifers_ = {
        "output": lambda x: x,
        "input": lambda x: x,
        "data": lambda x: x
    }

    def _make_fields(cls, T):
        """
        Each HandShake implementation should define a dict of _field_names_ for
        the signals (e.g. "ready" and "valid").  For consistency, we define the
        output/input names in terms of a Producer (i.e. ReadyValid outputs a
        valid and inputs a ready).

        Each implementation should define a dict of _qualifiers_ used to
        qualify the ports for producer, consumer, etc...
        """
        fields = {
            cls._field_names_["handshake_output"]:
                cls._qualifers_["output"](Bit),
            cls._field_names_["handshake_input"]:
                cls._qualifers_["input"](Bit)
        }
        _maybe_add_data(cls, fields, T, cls._qualifers_["data"])
        return fields

    def __getitem__(cls, T: Union[Type, MagmaProtocol]):
        assert cls._field_names_ is not None, "Undefined field name impl"
        fields = cls._make_fields(T)

        bases = (cls, )
        if hasattr(cls, "Base_T"):
            # Qualified variants include the unqualified type as a base class.
            # e.g. Producer(ReadyValid[Bits[8]]) will be a subtype of
            # ReadyValid[Bits[8]].
            bases += (cls.Base_T[T], )
        name = f"{cls}[{T}]"

        # Populates namespace for proper cache behavior (based on
        # hwtypes.adt_meta logic).
        ns = {}
        ns['__module__'] = cls.__module__
        name = f'{cls}[{T}]'
        ns['__qualname__'] = name

        # _cache_handler is implemented in hwtypes.adt_meta.
        return cls._cache_handler(True, fields, name, bases, ns)

    def __new__(mcs, name, bases, namespace, fields=None, **kwargs):
        cls = super().__new__(mcs, name, bases, namespace, fields, **kwargs)

        if not cls._field_names_:
            # Skip for base class (variants already exist and pointer is not
            # needed).
            return cls

        variants = (HandShakeMonitor, HandShakeDriver, HandShakeConsumer,
                    HandShakeProducer)
        if issubclass(cls, variants):
            return cls  # these don't need variants

        # Metaprogram variants for base type (e.g. for ReadyValid[Bits[8]],
        # create Producer(ReadyValid[Bits[8]])).
        for variant in variants:
            # Strip "HandShake" prefix for string name.
            suffix = f"{variant.__name__}"[len("HandShake"):]

            # Make variant type with appropriate base classes.
            variant_T = type(f"{suffix}({cls.__name__})",
                             (variant, cls), {})

            # Store pointer to variant (used by qualifiers).
            setattr(cls, f"{suffix}_T", variant_T)
            variant_T.Base_T = cls  # store pointer to base type

        return cls

    def flip(cls):
        raise TypeError(f"Cannot flip {cls.__name__} (undirected)")

    def qualify(cls, direction):
        if direction is Direction.In:
            return Monitor(cls)
        if direction is Direction.Out:
            return Driver(cls)
        if direction is Direction.Undirected:
            return Undirected(cls)
        raise TypeError(f"Cannot qualify {cls.__name__} with {direction}")

    @property
    def undirected_data_t(cls):
        try:
            data = cls.field_dict["data"]
        except KeyError:
            return None
        return data.undirected_t

    def __str__(cls):
        return cls.__name__


class HandShake(Product, metaclass=HandShakeKind):
    _field_names_ = None  # must be defined by implementation

    def fired(self):
        """
        Returns a bit that is high when ready and valid are both high.
        """
        raise NotImplementedError


class HandShakeProducerKind(HandShakeKind):
    _qualifers_ = {"output": Out, "input": In, "data": Out}

    def __getitem__(cls, T: Union[Type, MagmaProtocol]):
        t = super().__getitem__(T)
        if T is None:
            # Remove deq/no_deq methods if no data.
            t.deq = _deq_error
            t.no_deq = _no_deq_error
        return t

    def flip(cls):
        return Consumer(cls)


class HandShakeConsumerKind(HandShakeKind):
    _qualifers_ = {"output": In, "input": Out, "data": In}

    def __getitem__(cls, T: Union[Type, MagmaProtocol]):
        t = super().__getitem__(T)
        if T is None:
            t.enq = _enq_error
            t.no_enq = _no_enq_error
        return t

    def flip(cls):
        return Producer(cls)


class HandShakeConsumer(HandShake, metaclass=HandShakeConsumerKind):
    def fired(self):
        if not self.valid.driven():
            raise ReadyValidException(
                "Cannot invoke fired on consumer when valid isn't driven"
            )

        return self.ready & self.valid.value()

    def enq(self, value, when=True):
        """
        Produces the data `value` when `when` is high.

        Uses "last connect semantics", which allows multiple `enq` methods to
        be invoked with different conditions with precedence given to the later
        invocations.
        """
        if when is not True:
            if not (self.valid.driven() and self.data.driven()):
                raise ReadyValidException(
                    "Cannot use enq when without default driver"
                )
            curr_valid = self.valid.value()
            when |= curr_valid
            self.valid.unwire(curr_valid)

            curr_data = self.data.value()
            value = mux([curr_data, value], when)
            self.data.unwire(curr_data)
        self.valid @= when
        self.data @= value
        return value

    def no_enq(self, when=True):
        """
        Indicates no enqueue occurs.  Valid is set to false, and bits are
        connected to 0. (TODO: Should be an unitialized wire (Don't Care))
        """
        if when is not True:
            if not (self.valid.driven() and self.data.driven()):
                raise ReadyValidException(
                    "Cannot use no_deq with condition without an existing"
                    "valid and data driver"
                )
            valid = self.valid.value()
            data = self.data.value()
            self.valid.unwire(valid)
            self.data.unwire(data)
            self.valid @= mux([valid, False], when)
            self.data @= mux([data, 0], when)
        else:
            self.valid @= False
            self.data @= 0


class HandShakeProducer(HandShake, metaclass=HandShakeProducerKind):
    def fired(self):
        if not self.ready.driven():
            raise ReadyValidException(
                "Cannot invoke fired on producer when ready isn't driven"
            )
        return self.ready.value() & self.valid

    def deq(self, when=True):
        """
        Assert ready on this port and return associated data when `when` is
        high.

        This is typically used when valid has been asserted on the producer
        side.
        """
        if when is not True:
            if not self.ready.driven():
                raise ReadyValidException(
                    "Cannot use deq with when without a default ready driver"
                )
            ready = self.ready.value()
            self.ready.unwire(ready)
            self.ready @= ready | when
        else:
            self.ready @= when
        return self.data

    def no_deq(self, when=True):
        """
        Indicates no dequeue occurs, ready is set to False.
        """
        if when is not True:
            if not self.ready.driven():
                raise ReadyValidException(
                    "Cannot use no_deq with condition without an existing"
                    " ready driver"
                )
            ready = self.ready.value()
            self.ready.unwire(ready)
            self.ready @= mux([ready, False], when)
        else:
            self.ready @= False


class HandShakeMonitorKind(HandShakeKind):
    _qualifers_ = {"output": In, "input": In, "data": In}

    def flip(cls):
        return Driver(cls)


class HandShakeMonitor(HandShake, metaclass=HandShakeMonitorKind):
    pass


class HandShakeDriverKind(HandShakeKind):
    _qualifers_ = {"output": Out, "input": Out, "data": Out}

    def flip(cls):
        return Monitor(cls)


class HandShakeDriver(HandShake, metaclass=HandShakeDriverKind):
    pass


class ReadyValid(HandShake):
    """
    An I/O Bundle containing 'valid' and 'ready' signals that handshake
    the transfer of data stored in the 'data' subfield.

    The base protocol is undirected and is meant to be used with the modifiers:
    * m.Consumer(m.ReadyValid[T])  # data/valid are inputs, ready is output
    * m.Producer(m.ReadyValid[T])  # data/valid are outputs, ready is input

    T is the type of data to be wrapped in Ready/Valid.

    To create a ReadyValid type with no data, use T=None.  In this case, there
    will be no data port.

    The actual semantics of ready/valid are enforced via the use of concrete
    subclasses.
    """
    _field_names_ = {"handshake_output": "valid", "handshake_input": "ready"}


class Decoupled(ReadyValid):
    """
    `valid` indicates the prdoucer has put valid data in `data`, and `ready`
    indicates that the consumer is ready to accept the data this cycle.  No
    requirements are made on the signaling of ready or valid.
    """
    # TODO: Add down convert logic from Irrevocable consumer to Decoupled,
    # dropping guarantees of irrevocability.  Cannot be used on producer
    pass


class EnqIO(Decoupled.Producer_T):
    """
    Alias for Producer(Decoupled[T]).

    drives (outputs) `valid` and `data`, inputs `ready`.
    """
    pass


class DeqIO(Decoupled.Consumer_T):
    """
    Alias for Consumer(Decoupled[T]).

    drives (outputs) `ready`, inputs `valid` and `data`.
    """
    pass


class Irrevocable(ReadyValid):
    """
    Promises not to change the value of `data` after a cycle where `valid` is
    high and `ready` is low.  Additionally, once `valid` is raised, it will
    never be lowered until after `ready` has also been raised.
    """
    # TODO: Add upconvert logic from Decoupled producer to Irrevocable (can use
    # Irrevocable where a Decoupled is expected). Cannot be used on consumer.
    pass


class CreditValid(HandShake):
    _field_names_ = {"handshake_output": "valid", "handshake_input": "credit"}


def Consumer(T: HandShakeKind):
    if not issubclass(T, HandShake):
        raise TypeError(f"Consumer({T}) is unsupported")
    undirected_T = T.undirected_data_t
    return T.Consumer_T[undirected_T]


def Producer(T: HandShakeKind):
    if not issubclass(T, HandShake):
        raise TypeError(f"Producer({T}) is unsupported")
    undirected_T = T.undirected_data_t
    return T.Producer_T[undirected_T]


def Monitor(T: HandShakeKind):
    if not issubclass(T, HandShake):
        raise TypeError(f"Monitor({T}) is unsupported")
    undirected_T = T.undirected_data_t
    return T.Monitor_T[undirected_T]


def Driver(T: HandShakeKind):
    if not issubclass(T, HandShake):
        raise TypeError(f"Driver({T}) is unsupported")
    undirected_T = T.undirected_data_t
    return T.Driver_T[undirected_T]


def Undirected(T: HandShakeKind):
    if not issubclass(T, HandShake):
        raise TypeError(f"Undirected({T}) is unsupported")
    if not hasattr(T, 'Base_T'):
        return T  # already undirected
    undirected_T = T.undirected_data_t
    return T.Base_T[undirected_T]


def is_producer(T):
    return isinstance(T, (HandShakeProducerKind, HandShakeProducer))


def is_consumer(T):
    return isinstance(T, (HandShakeConsumerKind, HandShakeConsumer))


# TODO: QueueIO and Queue
