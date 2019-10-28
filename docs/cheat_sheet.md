**NOTE** This is a work in progress, please let us know via issue/gitter/email
if you'd like to see anything added to this.

This is inspired by https://github.com/freechipsproject/chisel-cheatsheet and
will be rendered in a similar single page layout soon.

# Basic Magma Constructs
Magma Values
```
class Test(Circuit):
    IO = ["I", In(Bits[5]), "O", Out(Bits[5])]

    @classmethod
    def definition(io):
        # Allocate `x` as a value of type `Bits`
        x = Bits[5]()
        # Wire io.I to x
        x <= io.I
        # Wire x to io.O
        io.O <= x
```

**NOTE** Currently magma only supports wiring two intermediate temporary values
if the driver already has a driver.  The following example will work, because `y` is 
driven by `io.I` before wiring to the temporary `x`.

```python
class Test(Circuit):
    IO = ["I", In(Bits[5]), "O", Out(Bits[5])]

    @classmethod
    def definition(io):
        x = Bits[5]()
        y = Bits[5]()
        y <= io.I
        x <= y
        io.O <= x
```
while this example will not work, because `y` has no driver when being wired to
`x`.  A fix for this issue is forthcoming.
```python
class Test(Circuit):
    IO = ["I", In(Bits[5]), "O", Out(Bits[5])]

    @classmethod
    def definition(io):
        x = Bits[5]()
        y = Bits[5]()
        y <= io.I
        x <= y
        io.O <= x
```

# When
**TODO**

# Switch
**TODO**

# Enum
```python
class State(m.Enum):
    zero = 0
    one = 1
    four = 4

class EnumExample(m.Circuit):
    IO = ["I", m.In(State), "O", m.Out(m.Array[2, State])]
    @classmethod
    def definition(io):
        io.O[0] <= io.I
        io.O[1] <= State.four
```

# Math Helpers
Contained in the module `magma.math`
* `log2_ceil(x: int) -> int` - `log2(x)` rounded up
* `log2_floor(x: int) -> int` - `log2(x)` rounded down
* `is_pow2(x: int) -> bool` - `True` if `x` is a power of 2

# Types
## Bit
* `m.Bit` - boolean value
* `m.VCC, m.GND` - boolean literals

## Array
* `m.Array[N, T]` - fixed length array of length `N` containing values of type
  `T` with equality operator (`==`) defined
* `m.array(value, n=None)` - convert `value` to an array.  `value` must be a
  magma type (`Bit`, `Tuple`, `Array`), a Python integer (e.g. literal), or a Python
  sequence (e.g. list).  If `n` is `None`, the width of the Array is inferred
  from `value` (e.g. length of the list, bit_length of the integer, length of
  the magma type)
* `m.Bits[N]` - length `N` bit vector with bitwise logical operators defined
* `m.bits(value, n=None)` - convert `value` to an `Bits` (same rules as
  `m.array` except if the input is a magma type or list, the members must be
  convertible to a Bit (e.g. Bit, bool, 0, 1))
* `m.UInt[N]` - length `N` unsigned integer that includes Bits operators and
  adds unsigned arithmetic (e.g. `+`, `-`, ...) and comparison operators (e.g.
  `<`, `<=`, ...)
* `m.uint(value, n=None)` - convert `value` to an `UInt` (same rules as
  `m.bits` except will not convert `m.SInt` to `m.UInt`)
* `m.SInt[N]` - length `N` signed integer that includes Bits operators and
  adds signed arithmetic (e.g. `+`, `-`, ...) and comparison operators (e.g.
  `<`, `<=`, ...)
* `m.sint(value, n=None)` - convert `value` to an `SInt` (same rules as
  `m.bits` except will not convert `m.UInt` to `m.SInt`)

## Tuple
* `m.Tuple(t0,t1,...)` - heterogenous compound aggregate datat type containing members
  of type `t0`, `t1`, ...  The anonymous variant uses integer keys like
  Python's tuple (i.e. for a tuple value `x`, `type(x[0]) == t0` and
  `type(x[1]) == t1`)
* `m.Tuple(k0=t0,k1=t1)` - same as anonymous variant except uses named keys ala
  Python's `namedtuple` (i.e. `type(x.k0) == t0`)

# Registers
Retain state until updated
```python
my_reg = mantle.Register(32)
my_reg_init_7 = mantle.Register(32, init=7)
my_reg_clock_enable = mantle.Register(32, init=7, has_ce=True)
```
Define update value by wiring to the input `I` port
```
my_reg.I <= next_val
```
Set `N` to `None` for a Register of a single `Bit` (setting `N` to `1` will
produce a register of `Bits[1]`)
```python
bit_reg = mantle.Register(None)
```

# Memories
```python
MyMemCircuit = mantle.DefineMemory(height, width, readonly=False, read_latency=0)
my_mem_inst = MyMemCircuit()
```
* `height` - number of elements
* `width` - width of each element
* `readonly` - ROM if True else RAM
* `read_latency` - number of registers to append to read out port

Ports
`addr_width = max((height - 1).bit_length(), 1)` 
* `RADDR` - `In(Bits[addr_width])`
* `RDATA` - `Out(Bits[width])`
* `WADDR` - `In(Bits[addr_width])`
* `WDATA` - `In(Bits[width])`
* `CLK` - `In(Clock)`
* `WE` - `In(Bit)`
