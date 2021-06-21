# magma Primitives
magma defines a core set of primitive generators that are parametrized over a
type `T` as well as some useful functions for working with magma types.

## Primitive Generators
### Register
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

### Memory
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

The memory provides a convenience interface following the Python
`__getitem__`/`__setitem__` pattern, here is an example:

```python
class MemoryGetItemSetItem(m.Circuit):
    io = m.IO(
        raddr=m.In(m.Bits[2]),
        rdata=m.Out(m.Bits[5]),
        waddr=m.In(m.Bits[2]),
        wdata=m.In(m.Bits[5]),
        clk=m.In(m.Clock),
        wen=m.In(m.Enable)

    )
    Mem4x5 = m.Memory(4, m.Bits[5])()
    io.rdata @= Mem4x5[io.raddr]
    Mem4x5[io.waddr] @= io.wdata
```

Reading from a memory using the `__getitem__` syntax (e.g. `Mem4x5[io.raddr]`)
is equivalent to wiring the `RADDR` port to the `__getitem__` key/index and
returning the `RDATA` port.  Note that writing to a memory uses `@=` with
`__getitem__` on the left hand side (as opposed to the standard `=` and
`__setitem__` pattern used in Python).  This is so that writing to a memory is
consistent with standard wiring using the `@=` syntax.  Writing to a memory
(e.g. `Mem4x5[io.waddr] @= io.wdata`) is equivalent to wiring the key/index
(`io.waddr`) to the `WADDR` port and the value (`io.wdata`) to the `WDATA`
port.

### Mux
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

## Dict and List Lookup
`magma` provides the helper functions `dict_lookup` and `list_lookup` to
facilitate mux generation for looking up values stored in a dictionary or list.

Here are the interfaces to the functions:
```python
def dict_lookup(dict_, select, default=0):
    """
    Use `select` as an index into `dict` (similar to a case statement)

    `default` is used when `select` does not match any of the keys and has a
    default value of 0
    """

def list_lookup(list_, select, default=0):
    """
    Use `select` as an index into `list` (similar to a case statement)

    `default` is used when `select` does not match any of the indices (e.g.
    when the select width is longer than the list) and has a default value of
    0.
    """
```

Here's examples of using them:
```python
class DictLookup(m.Circuit):
    io = m.IO(S=m.In(m.Bits[2]), O=m.Out(m.Bits[5]))

    dict_ = {
        0: BitVector[5](0),
        2: BitVector[5](2),
        3: BitVector[5](3)
    }
    io.O @= m.dict_lookup(dict_, io.S, default=BitVector[5](1))


class ListLookup(m.Circuit):
    io = m.IO(S=m.In(m.Bits[2]), O=m.Out(m.Bits[5]))

    list_ = [BitVector[5](0), BitVector[5](1), BitVector[5](2)]
    io.O @= m.list_lookup(list_, io.S, default=BitVector[5](3))
```


### LUT
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

## Functions
### reduce (bitwise)
The `m.reduce` function allows you to apply a reduction operator on a value of
type `Bits`.  Here's a simple example:
```python
import operator
import magma as m

class ReduceAnd(m.Circuit):
    io = m.IO(I=m.In(m.Bits[5]), O=m.Out(m.Bit))
    io.O @= m.reduce(operator.and_, io.I)
```
The `m.reduce` function will generate an instance of the coreir bitwise reduce
primitive, which will in turn compile to a verilog bitwise reduction (e.g.
`assign O = &I`).

For convenience, we also provide the following methods on the Bits type:
* `reduce_and()` - shorthand for `m.reduce(operator.and_, bits_value)`
* `reduce_or()` - shorthand for `m.reduce(operator.or_, bits_value)`
* `reduce_xor()` - shorthand for `m.reduce(operator.xor, bits_value)`

For other reduction patterns (non-bitwise), you can simply use the standard
`functools.reduce`.

Reduce interface: `reduce(operator, bits: Bits)`

### get_slice and set_slice
These operators provide a functional-style syntax for working with dynamic
slices of magma arrays.  They allow you to use a dynamic slice start index with
a constant width (e.g. get a slice of 8 bits starting at index `x` where `x` is
an input to the circuit).  We choose this explicit functional style syntax to
constrain the support of dynamic slicing to constant widths.  For non-dynamic
slicing (i.e. the start and stop are known at compile time), you can simply use
the built-in slice syntax `[start:stop]`.  magma does not support dynamic width
slicing.

Here's two simple slice examples:
```python
class GetSlice(m.Circuit):
    io = m.IO(
        I=m.In(m.Bits[10]),
        x=m.In(m.Bits[2]),
        O=m.Out(m.Bits[6])
    )
    # O will output the 6 bits starting at index io.x
    io.O @= m.get_slice(io.I, start=io.x, width=6)

class SetSlice(m.Circuit):
    io = m.IO(
        I=m.In(m.Bits[6]),
        x=m.In(m.UInt[2]),
        O=m.Out(m.Bits[12])
    )

    # default value
    O = m.Bits[12](0xFFF)
    # O will output 0xFF except with the 6 bits start at index x replaced with
    # the value of io.I
    io.O @= m.set_slice(O, io.I, start=io.x, width=6)
```

Slice function interfaces:
* `get_slice(value: Bits, start: Bits, width: int)` - Dynamic slice of `value` based off
  the dynamic value of `start` and the constant value of `width`.
* `set_slice(target: Bits, value: Bits, start: UInt, width: int)`
   * target: the output with a dynamic slice range replaced by value
   * value: the output driving a slice of target
   * start: dynamic start index of the slice
   * width: constant slice width


### set_bit
Similar to set_slice/get_slice, this function allows you to dynamically set the
value of a bit in a Bits value.  Here's an example:

```python
class SetBit(m.Circuit):
    io = m.IO(I=m.In(m.Bits[4]),
              val=m.In(m.Bit),
              idx=m.In(m.Bits[2]),
              O=m.Out(m.Bits[4]))
    io.O @= m.set_bit(io.I, io.val, io.idx)
```

Interface:
```python
def set_bit(target: Bits, value: Bit, idx: UInt):
    """
    Returns a new value where index `idx` of value `target` is set to `value`
    """
```
