from typing import Union
from magma.bit import Bit
from magma.logging import root_logger
from magma.primitives.mux import mux
from magma.t import Type, In, Out, Flip
from magma.protocol_type import MagmaProtocol
from magma.tuple import Product, ProductKind


_logger = root_logger()


class ReadyValidException(Exception):
    pass


class ReadyValidKind(ProductKind):
    def _check_T(cls, T):
        if not issubclass(T, (Type, MagmaProtocol)):
            raise TypeError(
                f"{cls}[T] expected T to be a subclass of m.Type or"
                f" m.MagmaProtocol not {T}"
            )
        undirected_T = T.as_undirected()
        if undirected_T is not T:
            _logger.warning(
                f"Type {T} used with ReadyValid is not undirected, converting"
                " to undirected type"
            )
        return undirected_T

    def __getitem__(cls, T: Union[Type, MagmaProtocol]):
        T = cls._check_T(T)
        fields = {"valid": Bit, "data": T, "ready": Bit}
        return type(f"{cls}[{T}]", (cls, ), fields)


class ReadyValid(Product, metaclass=ReadyValidKind):
    """
    An I/O Bundle containing 'valid' and 'ready' signals that handshake
    the transfer of data stored in the 'data' subfield.

    The base protocol is undirected and is meant to be used with the modifiers:
    * m.Consumer(m.ReadyValid[T])  # data/valid are inputs, ready is output
    * m.Producer(m.ReadyValid[T])  # data/valid are outputs, ready is input

    T is the type of data to be wrapped in Ready/Valid

    The actual semantics of ready/valid are enforced via the use of concrete
    subclasses.
    """
    def fired(self):
        """
        Returns a bit that is high when ready and valid are both high
        """
        raise NotImplementedError


class ReadyValidProducerKind(ReadyValidKind):
    def __getitem__(cls, T: Union[Type, MagmaProtocol]):
        T = cls._check_T(T)
        fields = {"valid": Out(Bit), "data": Out(T), "ready": In(Bit)}
        return type(f"{cls}[{T}]", (cls, ), fields)


class ReadyValidProducer(ReadyValid, metaclass=ReadyValidProducerKind):
    def fired(self):
        """
        Returns a bit that is high when ready and valid are both high
        """
        if not self.valid.driven():
            raise ReadyValidException(
                "Cannot invoke fired on producer when valid isn't driven"
            )
        return self.valid.value() & self.ready

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


class ReadyValidConsumerKind(ReadyValidKind):
    def __getitem__(cls, T: Union[Type, MagmaProtocol]):
        T = cls._check_T(T)
        fields = {"valid": In(Bit), "data": In(T), "ready": Out(Bit)}
        return type(f"{cls}[{T}]", (cls, ), fields)


class ReadyValidConsumer(ReadyValid, metaclass=ReadyValidConsumerKind):
    def fired(self):
        if not self.ready.driven():
            raise ReadyValidException(
                "Cannot invoke fired on consumer when ready isn't driven"
            )

        return self.valid & self.ready.value()

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


def Consumer(T: ReadyValidKind):
    if issubclass(T, ReadyValid):
        return ReadyValidConsumer[T.data.as_undirected()]
    raise TypeError(f"Consumer({T}) is unsupported")


def Producer(T: ReadyValidKind):
    if issubclass(T, ReadyValid):
        return ReadyValidProducer[T.data.as_undirected()]
    raise TypeError(f"Consumer({T}) is unsupported")
