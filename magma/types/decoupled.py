import magma as m
from magma.tuple import Product, ProductKind


from magma.bit import Bit
from magma.t import Type, In, Out
from magma.tuple import Product, ProductKind


class ReadyValidException(Exception):
    pass


class ReadyValidKind(ProductKind):
    def __getitem__(cls, T: Type):
        if not issubclass(T, Type):
            raise TypeError(
                f"ReadyValid[T] expected T to be a subclass of m.Type not {T}"
            )
        fields = {"valid": Out(Bit), "data": Out(T), "ready": In(Bit)}
        return type(f"ReadyValid[{T}]", (ReadyValid, ), fields)


class ReadyValid(Product, metaclass=ReadyValidKind):
    """
    An I/O Bundle containing 'valid' and 'ready' signals that handshake
    the transfer of data stored in the 'data' subfield.

    The base protocol implied by the directionality is that
    the producer uses the interface as-is (outputs bits)
    while the consumer uses the flipped interface (inputs bits).

    For readability, we provide these helpers to avoid the confusion related to
    In versus Out:
    * m.Consume(m.ReadyValid[T])
    * m.Product(m.ReadyValid[T])

    T is the type of data to be wrapped in Ready/Valid

    The actual semantics of ready/valid are enforced via the use of concrete
    subclasses.
    """
    def fired(self):
        """
        Returns a bit that is high when ready and valid are both high
        """
        if self.is_consumer():
            if not self.ready.driven():
                raise ReadyValidException(
                    "Cannot invoke fired on consumer when ready isn't driven"
                )

            return self.valid & self.ready.value()

        assert self.is_producer()
        if not self.valid.driven():
            raise ReadyValidException(
                "Cannot invoke fired on consumer when valid isn't driven"
            )
        return self.valid.value() & self.ready

    def enq(self, value, when=True):
        """
        Produces the data `value` when `when` is high

        Uses "last connect semantics", which allows multiple `enq` methods to
        be invoked with different conditions with precedence given to the later
        invocations.
        """
        if not self.is_producer():
            raise TypeError("Cannot invoke enq on consumer")
        if when is not True:
            if not (self.valid.driven() and self.data.driven()):
                raise ReadyValidException(
                    "Cannot use enq when without default driver"
                )
            curr_valid = self.valid.value()
            when |= curr_valid
            self.valid.unwire(curr_valid)

            curr_data = self.data.value()
            value = m.mux([curr_data, value], when)
            self.data.unwire(curr_data)
        self.valid @= when
        self.data @= value
        return value

    def no_enq(self, when=True):
        """
        Indicates no enqueue occurs.  Valid is set to false, and bits are
        connected to 0 (TODO: Should be an unitialized wire (Don't Care))
        """
        if not self.is_producer():
            raise TypeError("Cannot invoke no_enq on consumer")
        if when is not True:
            if not (self.valid.driven() and self.data.driven()):
                raise ReadyValidException(
                    "Cannot use no_deq with condition without an existing valid"
                    " and data driver"
                )
            valid = self.valid.value()
            data = self.data.value()
            self.valid.unwire(valid)
            self.data.unwire(data)
            self.valid @= m.mux([valid, False], when)
            self.data @= m.mux([data, 0], when)
        else:
            self.valid @= False
            self.data @= 0

    def deq(self, when=True):
        """
        Assert ready on this port and return associated data when `when` is
        high

        This is typically used when valid has been asserted on the producer
        side.
        """
        if not self.is_consumer():
            raise TypeError("Cannot invoke deq on producer")
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
        Indicates no dequeue occurs, ready is set of False
        """
        if not self.is_consumer():
            raise TypeError("Cannot invoke no_deq on producer")
        if when is not True:
            if not self.ready.driven():
                raise ReadyValidException(
                    "Cannot use no_deq with condition without an existing"
                    " ready driver"
                )
            ready = self.ready.value()
            self.ready.unwire(ready)
            self.ready @= m.mux([ready, False], when)
        else:
            self.ready @= False

    def is_producer(self):
        return self.valid.is_input()

    def is_consumer(self):
        return self.valid.is_output()


def Consume(T: ReadyValidKind):
    if not isinstance(T, ReadyValidKind):
        raise TypeError("Consume can only be used with ReadyValid Types")
    return m.Flip(T)


def Produce(T: ReadyValidKind):
    if not isinstance(T, ReadyValidKind):
        raise TypeError("Produce can only be used with ReadyValid Types")
    return T
