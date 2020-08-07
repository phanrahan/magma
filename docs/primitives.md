# magma Primitives
magma defines a core set of primitives that are parametrized over a type `T`.

# Register
The `Register(T)` primitive creates a register circuit that stores a value of
type `T`.  Here's a simple example that delays an input byte by a cycle.

```python
import magma as m
from magma.primitives import Register


class DelayByteByOneCycle(m.Circuit):
    io = m.IO(I=m.In(m.Bits[8]), O=m.Out(m.Bits[8])) 
    io += m.ClockIO(has_reset=True)
    io.O @= Register(m.Bits[8], m.Bits[8](0xDE), reset_type=m.Reset)()(io.I)
```

Register `__init__` arguments:
* `T: m.Kind` - The type of the value stored in the register (e.g. `Bits[5]`)
* `init: Union[m.Type, int]` - (optional) A const value (i.e. init.const() ==
                                True) of type T or an int to be used as the
                                initial value of the register.  If no value is
                                provided, the register will be initialized with
                                0.
* `has_enable: bool` - (optional) whether the register has an enable signal
* `reset_type: m.AbstractReset` - (optional) The type of the reset port 
                                  (also specifies the semantic behavior of the
                                  reset signal)
* `reset_priority: bool` - (optional) boolean flag choosing whether synchronous
                           reset (RESET or RESETN) has priority over enable

# Memory
The `Memory(N, T)` primitive creates a one read port and one write port memory
storing `N` values of type `T`.  Here's a simple example that generates a
memory with 4 entries, each contain 5 bits:
```python
class SimpleMem(m.Circuit):
    io = m.IO(
        raddr=m.In(m.Bits[2]),
        rdata=m.Out(m.Bits[5]),
        waddr=m.In(m.Bits[2]),
        wdata=m.In(m.Bits[5]),
        clk=m.In(m.Clock),
        wen=m.In(m.Enable)

    )
    Mem4x5 = m.Memory(4, m.Bits[5])()
    Mem4x5.RADDR @= io.raddr
    io.rdata @= Mem4x5.RDATA
    Mem4x5.WADDR @= io.waddr
    Mem4x5.WDATA @= io.wdata
```

Mem `__init__` arguments:
* `height: int` - number of entries in the memory
* `T: m.Kind` - type of each entry
* `read_latency: int` - (optional, default 0) the number of cycles it takes for
                        a value to appear on the read port.
* `read_only: bool` - (optional, default False) set to True to disable the
                      generation of a write port
* `init: Optional[tuple]` - (optional) initial contents of the memory as a
                            tuple containing an initial value for each entry 

# Mux
The `Mux(N, T)` primitive creates a mux circuit that selects between `N` input
values of type `T`.  Here's a simple example that selects between two bits:
```python
class SelectABit(m.Circuit):
    io = m.IO(I=m.In(m.Bits[2]), S=m.In(m.Bit), O=m.Out(m.Bit))
    io.O @= Mux(2, m.Bit)()(io.I[0], io.I[1], io.S)
```

Mux `__init__` arguments:
* `height: int` - number of inputs to select from
* `T: m.Kind` - type of the input values

The generated mux circuit will have separate ports for each input (i.e. `I0`
for the 1st input, `I1` for the second...).  The select input will select
the input value in ascending order (`S == 0` will select `I0`, `S == 1` will
select `I1`, ...).

# LUT
The `LUT(T, contents)` primitive creates a lookup table circuit programmed with
`contents` (a tuple of values of type T).
Here's a simple example with 4 entries of 8-bit values:
```python
contents = (
    m.Bits[8](0xDE),
    m.Bits[8](0xAD),
    m.Bits[8](0xBE),
    m.Bits[8](0xEF)
)

class SimpleLUT(m.Circuit):
    io = m.IO(I=m.In(m.Bits[2]), O=m.Out(m.Bits[8]))
    io.O @= LUT(m.Bits[8], contents)()(io.I)
```

LUT `__init__` arguments:
* `T: m.Kind` - type of the lookup table contents
* `contents` - the contents of the LUT (a tuple containing
              elements of type T that are constant)
