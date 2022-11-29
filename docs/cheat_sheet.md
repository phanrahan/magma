**NOTE**: This is a work in progress, please let us know via issue/gitter/email
if you'd like to see anything added to this.

This is inspired by the [chisel cheatsheet](https://github.com/freechipsproject/chisel-cheatsheet)
and will be rendered in a similar single page layout soon.

# Types
## Bit
* `m.Bit`: boolean value
* `m.VCC, m.GND`: boolean literals

## Bits and Integers
* `m.Bits[N]`: length `N` bit vector with bitwise logical operators defined
* `m.UInt[N]`: length `N` unsigned integer that includes Bits operators and
  unsigned arithmetic (e.g. `+`, `-`, ...) and comparison operators (e.g.
  `<`, `<=`, ...)
* `m.SInt[N]`: length `N` signed integer that includes Bits operators and
  signed arithmetic (e.g. `+`, `-`, ...) and comparison operators (e.g.
  `<`, `<=`, ...)

## Array
* `m.Array[N, T]`: fixed length array of length `N` containing values of type
  `T` with equality operator (`==`) defined

## Tuples and Products
* `m.Tuple[t0, t1, ...]`: heterogenous compound data type containing members of
  type `t0`, `t1`, ... Values of such types can be indexed using integer keys
  like Python tuples (e.g. for a tuple value `x`, `type(x[0]) == t0`).
* `m.Product.from_fields(name, dict(k0=t0, k1=t1, ...))`: heterogenous compound
  data type containing members of type `t0`, `t1`, ... Values of such types can
  be indexed using attributes (e.g. for a product value `x`, `type(x.k0) ==
  t0`). `name="anon"` makes this type anonymous.
  * Alternate syntax:
  ```python
  class <name>(m.Product):
      k0 = t0
      k1 = t1
      ...
  ```

## Enum
Statically typed enumerated type:
```python
class <name>(m.Enum):
    k0 = v0
    k1 = v1
    ...

```

Example
```python
class State(m.Enum):
    IDLE = 0
    CONFIG = 1
    LOOP = 2
    FLAG_RESET = 3

class LoopState(m.Enum):
    LOOP_READ = 0
    LOOP_STIM = 1
```

# Type qualifiers
`m.In(T)`, `m.Out(T)`, `m.InOut(T)` qualify type `T` to be an input, output, and
inout respectively.

# Type conversions
* `m.bits(value, n=None)`: convert `value` to an `Bits` (same rules as
  `m.array` except if the input is a magma type or list, the members must be
  convertible to a Bit (e.g. `Bit`, `bool`, `0`, `1`))
* `m.array(value, n=None)`: convert `value` to an array.  `value` must be a
  magma type (`Bit`, `Tuple`, `Array`), a Python integer (e.g. literal), or a Python
  sequence (e.g. list).  If `n` is `None`, the width of the array is inferred
  from `value` (e.g. length of the list, bit length of the integer, length of
  the magma type)
* `m.uint(value, n=None)`: convert `value` to an `UInt` (same rules as
  `m.bits`, except will not convert `m.SInt` to `m.UInt`)
* `m.sint(value, n=None)`: convert `value` to an `SInt` (same rules as
  `m.bits`, except will not convert `m.UInt` to `m.SInt`)

# Registers
Retain state until updated:
```python
# Note that m.Register is a generator, which returns a circuit, which is then
# instanced
my_reg = m.Regester(m.Bits[32])()
my_reg_init_7 = m.Register(m.Bits[32], init=7)()
my_reg_clock_enable = m.Register(m.Bits[32], init=7, has_enable=True)()
my_reg_uint = m.Register(m.UInt[32], init=7, has_enable=True)()
```
Define update value by wiring to the input `I` port
```
my_reg.I @= next_val
```

# Memories
```python
MyMemCircuit = m.Memory(height, T, read_latency=0, readonly=False, init=None,
                        has_read_enable=False)
my_mem_inst = MyMemCircuit()
```
* `height`: number of elements
* `T`: type of each element
* `readonly`: ROM if True else RAM
* `init`: `tuple` of initial values of each element
* `read_latency`: number of registers to append to read out port
* `has_read_enabe`: add a read enable port

Memory ports (where `addr_width = max(clog2(height - 1), 1)`):

* `RADDR`: `m.In(m.Bits[addr_width])`
* `RDATA`: `m.Out(T)`
* `WADDR`: `m.In(m.Bits[addr_width])`
* `WDATA`: `m.In(mT`
* `CLK`: `m.In(m.Clock)`
* `WE`: `m.In(m.Bit)`
* `RE` (optional): `m.In(m.Bit)`

# Circuits
**Defining**: subclass `m.Circuit`
```python
class Accum16(m.Circuit):
    io = m.IO(I=m.In(m.UInt[16]), O=m.Out(m.UInt[16])) + m.ClockIO()

    sum_ = m.Register(m.UInt[16])()
    io.O @= sum_(sum_.O + io.I)
```
**Usage**: circuits are used by instancing them inside another definitions and
  their ports are accessed using dot notation
```python
my_module = Accum16()
my_module.I @= some_data
sum_ = my_module.O
```

**Wiring**: wire an output to an input using `@=` operator (statically typed)

**Metaprogramming**: abstract over parameters by using a Generator2
```python
class Accum(m.Generator2):
   def __init__(self, width: int):
        self.io = m.IO(I=m.In(m.UInt[width]), O=m.Out(m.UInt[width])) + m.ClockIO()

        sum_ = m.Register(m.UInt[width])()
        io.O @= sum_(sum_.O + io.I)
Accum8 = Accum(8)
accum8_inst = Accum8()
```

# Operators
## Infix operators
All types support the following operators:
- Equal `==`
- Not Equal `!=`

The `Bit` type supports the following logical operators.
- And `&`
- Or `|`
- Exclusive or `^`
- Not `~`

The `Array` type family supports the following operator.
- Dynamic bit selection `my_arry[add.O]` (select a bit dynamically using a magma value).

The `Bits` type family supports the following logical operators.
- And `&` (element-wise)
- Or `|` (element-wise)
- Exclusive or `^` (element-wise)
- Not `~` (element-wise)
- Logical right shift (with zeros) `>>`
- Logical left shift (with zeros) `<<`

The `UInt` and `SInt` types support all the logical operators
as well as arithmetic and comparison operators.
- Add `+`
- Subtract/Negate `-`
- Multiply `*`
- Divide `/`
- Less than `<`
- Less than or equal `<=`
- Greater than `>`
- Greater than or equal `>=`

Note that the the right shift operator when applied to an `SInt` becomes
an arithmetic shift right operator (which replicates the sign bit as it shifts right).

## Functional operators
- `m.mux(*I, S)` (constraint: `len(S) == log2_ceil(len(I))`): select `I[S]`.
- `m.zext(v, n)`: zero extend array `v` by `n`
- `m.sext(v, n)`: sign extend array `v` by `n`
- `m.concat(*arrays)`: concat arrays together
- `m.repeat(value, n)`: create an array repeating `value` `n` times

# when
```python
class BasicWhen(m.Circuit):
    io = m.IO(I=m.In(m.Bits[2]), S=m.In(m.Bit), O=m.Out(m.Bit))
    with m.when(io.S):
        io.O @= io.I[0]
    with m.otherwise():
        io.O @= io.I[1]
```

# when with registers
```python
class RegDefault(m.Circuit):
    name = "test_when_reg_ce"
    io = m.IO(I=m.In(m.Bits[8]), O=m.Out(m.Bits[8]),
              CE=m.In(m.Bit))

    x = m.Register(m.Bits[8])()
    # Register implicit default is x.I @= x.O
    with m.when(io.CE):
        x.I @= io.I
    io.O @= x.O
```

# when with registers with enable
```python
class RegDefault(m.Circuit):
    name = "test_when_reg_ce"
    io = m.IO(I=m.In(m.Bits[8]), O=m.Out(m.Bits[8]),
              CE=m.In(m.Bit))

    x = m.Register(m.Bits[8], has_enable=True)()
    with m.when(io.CE):
        x.I @= io.I
        # x.CE will implicitly be 1 when written
    io.O @= x.O
```
