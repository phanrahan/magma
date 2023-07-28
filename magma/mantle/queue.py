"""
Based on
https://github.com/chipsalliance/chisel3/blob/master/src/main/scala/chisel3/util/Decoupled.scala
(missing support for `flow` and `pipe` parameters).
"""
import magma as m
from magma.mantle.counter import Counter


class Queue(m.Generator2):
    def __init__(self, entries: int, T: m.Kind):
        assert entries >= 0
        self.io = m.IO(
            # NOTE(leonardt): Note that the direction of enq/deq are flipped
            # since this is a client (consumer)
            enq=m.DeqIO[T],
            deq=m.EnqIO[T]
        ) + m.ClockIO()

        # Data storage
        ram = m.Memory(entries, T)()

        # Read/write pointers
        enq_ptr = Counter(entries, has_enable=True)()
        deq_ptr = Counter(entries, has_enable=True)()

        # Since the pointers can match when it's empty or full, we use an extra
        # bit to track when it may be full (there's been a write without a
        # read)
        maybe_full = m.Register(init=False, has_enable=True)()

        ptr_match = enq_ptr.O == deq_ptr.O
        # Empty/full determined by pointers matching and maybe_full bit
        empty = ptr_match & ~maybe_full.O
        full = ptr_match & maybe_full.O

        # deq data is valid when not empty
        self.io.deq.valid @= ~empty
        # enq is ready when not full
        self.io.enq.ready @= ~full

        # do enq/deq when ready/valid are high
        do_enq = self.io.enq.fired()
        do_deq = self.io.deq.fired()

        # write enq data when do_enq
        ram.write(self.io.enq.data, enq_ptr.O, m.enable(do_enq))

        # Increment pointers on read/write
        enq_ptr.CE @= m.enable(do_enq)
        deq_ptr.CE @= m.enable(do_deq)

        # Set maybe full when enq without deq
        maybe_full.I @= m.enable(do_enq)
        maybe_full.CE @= m.enable(do_enq != do_deq)

        # Deq data from storage
        self.io.deq.data @= ram[deq_ptr.O]
