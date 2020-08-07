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

# Mux
The `Mux(T)` primitive creates a mux circuit that selects between values of
type `T`.  Here's a simple example that selects between two bits:
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
