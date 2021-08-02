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


class ReadyValidKind(ProductKind):
    def __getitem__(cls, T: Union[Type, MagmaProtocol]):
        fields = {"valid": Bit, "ready": Bit}
        _maybe_add_data(cls, fields, T, lambda x: x)
        return type(f"{cls}[{T}]", (cls, ), fields)

    def flip(cls):
        raise TypeError("Cannot flip an undirected ReadyValid type")

    def qualify(cls, direction):
        if direction is Direction.In:
            return Monitor(cls)
        if direction is Direction.Undirected:
            return Undirected(cls)
        raise TypeError(f"Cannot qualify ReadyValid with {direction}")

    @property
    def undirected_data_t(cls):
        try:
            data = cls.field_dict["data"]
        except KeyError:
            return None
        return data.undirected_t


class ReadyValid(Product, metaclass=ReadyValidKind):
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

    def fired(self):
        """
        Returns a bit that is high when ready and valid are both high
        """
        raise NotImplementedError


def _deq_error(self, value, when=True):
    raise Exception(f"{type(self)} does not support deq")


def _no_deq_error(self, value, when=True):
    raise Exception(f"{type(self)} does not support no_deq")


class ReadyValidProducerKind(ReadyValidKind):
    def __getitem__(cls, T: Union[Type, MagmaProtocol]):
        fields = {"valid": Out(Bit), "ready": In(Bit)}
        _maybe_add_data(cls, fields, T, Out)
        t = type(f"{cls}[{T}]", (cls, cls.__bases__[-1][T],), fields)
        if T is None:
            # Remove deq/no_deq methods if no data.
            t.deq = _deq_error
            t.no_deq = _no_deq_error
        return t

    def flip(cls):
        return Consumer(cls)

    def __str__(cls):
        if not cls.is_bound:
            return cls.__name__
        return f"Producer(ReadyValid[{cls.undirected_data_t}])"


class ReadyValidProducer(ReadyValid, metaclass=ReadyValidProducerKind):
    def fired(self):
        """
        Returns a bit that is high when ready and valid are both high
        """
        if not self.ready.driven():
            raise ReadyValidException(
                "Cannot invoke fired on producer when ready isn't driven"
            )
        return self.ready.value() & self.valid

    def deq(self, when=True):
        """
        Assert ready on this port and return associated data when `when` is
        high

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
        Indicates no dequeue occurs, ready is set to False
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


def _enq_error(self, value, when=True):
    raise Exception(f"{type(self)} does not support enq")


def _no_enq_error(self, value, when=True):
    raise Exception(f"{type(self)} does not support no_enq")


class ReadyValidConsumerKind(ReadyValidKind):
    def __getitem__(cls, T: Union[Type, MagmaProtocol]):
        fields = {"valid": In(Bit), "ready": Out(Bit)}
        _maybe_add_data(cls, fields, T, In)
        t = type(f"{cls}[{T}]", (cls, cls.__bases__[-1][T],), fields)
        if T is None:
            t.enq = _enq_error
            t.no_enq = _no_enq_error
        return t

    def flip(cls):
        return Producer(cls)

    def __str__(cls):
        if not cls.is_bound:
            return cls.__name__
        return f"Consumer(ReadyValid[{cls.undirected_data_t}])"


class ReadyValidConsumer(ReadyValid, metaclass=ReadyValidConsumerKind):
    def fired(self):
        if not self.valid.driven():
            raise ReadyValidException(
                "Cannot invoke fired on consumer when valid isn't driven"
            )

        return self.ready & self.valid.value()

    def enq(self, value, when=True):
        """
        Produces the data `value` when `when` is high

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
        connected to 0 (TODO: Should be an unitialized wire (Don't Care))
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


class ReadyValidMonitorKind(ReadyValidKind):
    def __getitem__(cls, T: Union[Type, MagmaProtocol]):
        fields = {"valid": In(Bit), "ready": In(Bit)}
        _maybe_add_data(cls, fields, T, In)
        return type(f"{cls}[{T}]", (cls, ReadyValid[T]), fields)

    def flip(cls):
        raise TypeError("Cannot flip Monitor")

    def __str__(cls):
        if not cls.is_bound:
            return cls.__name__
        return f"Monitor(ReadyValid[{cls.undirected_data_t}])"


class ReadyValidMonitor(ReadyValid, metaclass=ReadyValidMonitorKind):
    pass


class Decoupled(ReadyValid):
    """
    `valid` indicates the prdoucer has put valid data in `data`, and `ready`
    indicates that the consumer is ready to accept the data this cycle.  No
    requirements are made on the signaling of ready or valid.
    """
    # TODO: Add down convert logic from Irrevocable consumer to Decoupled,
    # dropping guarantees of irrevocability.  Cannot be used on producer
    pass


class DecoupledConsumer(ReadyValidConsumer, Decoupled):
    pass


class DecoupledProducer(ReadyValidProducer, Decoupled):
    pass


class DecoupledMonitor(ReadyValidMonitor, Decoupled):
    pass


class EnqIO(DecoupledProducer):
    """
    Alias for Producer(Decoupled[T])

    drives (outputs) `valid` and `data`, inputs `ready`
    """
    pass


class DeqIO(DecoupledConsumer):
    """
    Alias for Consumer(Decoupled[T])

    drives (outputs) `ready`, inputs `valid` and `data`
    """
    pass


class Irrevocable(ReadyValid):
    """
    Promises not to change the value of `data` after a cycle where `valid` is
    high and `ready` is low.  Additionally, once `valid` is raised, it will
    never be lowered until after `ready` has also been raised
    """
    # TODO: Add upconvert logic from Decoupled producer to Irrevocable (can use
    # Irrevocable where a Decoupled is expected). Cannot be used on consumer.
    pass


class IrrevocableConsumer(ReadyValidConsumer, Irrevocable):
    pass


class IrrevocableProducer(ReadyValidProducer, Irrevocable):
    pass


class IrrevocableMonitor(ReadyValidMonitor, Decoupled):
    pass


def Consumer(T: ReadyValidKind):
    if issubclass(T, ReadyValid):
        undirected_T = T.undirected_data_t
    if issubclass(T, Irrevocable):
        return IrrevocableConsumer[undirected_T]
    if issubclass(T, Decoupled):
        return DecoupledConsumer[undirected_T]
    if issubclass(T, ReadyValid):
        return ReadyValidConsumer[undirected_T]
    raise TypeError(f"Consumer({T}) is unsupported")


def Producer(T: ReadyValidKind):
    if issubclass(T, ReadyValid):
        undirected_T = T.undirected_data_t
    if issubclass(T, Irrevocable):
        return IrrevocableProducer[undirected_T]
    if issubclass(T, Decoupled):
        return DecoupledProducer[undirected_T]
    if issubclass(T, ReadyValid):
        return ReadyValidProducer[undirected_T]
    raise TypeError(f"Consumer({T}) is unsupported")


def Monitor(T: ReadyValidKind):
    if issubclass(T, ReadyValid):
        undirected_T = T.undirected_data_t
    if issubclass(T, Irrevocable):
        return IrrevocableMonitor[undirected_T]
    if issubclass(T, Decoupled):
        return DecoupledMonitor[undirected_T]
    if issubclass(T, ReadyValid):
        return ReadyValidMonitor[undirected_T]
    raise TypeError(f"Monitor({T}) is unsupported")


def Undirected(T: ReadyValidKind):
    if issubclass(T, ReadyValid):
        undirected_T = T.undirected_data_t
    if issubclass(T, Irrevocable):
        return Irrevocable[undirected_T]
    if issubclass(T, Decoupled):
        return Decoupled[undirected_T]
    if issubclass(T, ReadyValid):
        return ReadyValid[undirected_T]
    raise TypeError(f"Undirected({T}) is unsupported")


# TODO: QueueIO and Queue
