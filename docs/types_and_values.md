## Magma Types and Values

Magma is a strongly typed language within python.
As in python, all Magma types are python classes.
Instances of Magma types are Magma values.

The first major set of types are single bit types. 
They are subclasses of `Digital`:
```python
class Digital(Type):
  class Bit(Digital):
  class Clock(Digital):
  class Reset(Digital):
  class Enable(Digital):
```
The `Bit` type can be used in logical operations.

The second major type in Magma is the `Array` type.
An `Array` consists of `N` values of the same type `T`.
```python
Array[N, T]
```

The third major type in Magma is the `Tuple` (and `Product`) type.
A `Tuple` consists of `N` unnamed values of different types `Tn`.
```python
Tuple[T0, T1, ..., Tn]
```
A `Product` consists of `n` named values of different types `Tn`.
```python
Product.from_fields(name, dict(name0=T0, name1=T1, ..., namen=Tn))
```

The `Bits` type is equivalent to an array of `Bit`.
It is a subclass of an array type.
The `UInt` and `SInt` types are used 
to represent unsigned and signed integer types.
`UInt` and `SInt` are subclasses of the `Bits` type.
`Bits`, `UInt`, and `SInt` are separate types 
because they support different operations.
```python
Bits[n] # ~= Array(n, Bit)
        # &, |, ^, ~, ==, <<, >>
SInt[n] # +, -, *, /, <, <=, >=, >, -, >>>
UInt[n] # +, -, *, /, <, <=, >=, >
```

Types can be tested for equality and inequality.

Values are instances of Magma type classes.
All values are subclasses of the Magma type `Type`.

## NDArray
Magma provides support numpy style NDArrays.  These types are constructed by
using a tuple of integers (e.g. `(3, 4, 2)`) for the `N` parameter of an Array.
Here's a simple example:

```python
class Main(m.Circuit):
    io = m.IO(I=m.In(m.Array[(3, 5), m.Bit]),
              O=m.Out(m.Array[(5, 3), m.Bit]))
    for i in range(3):
        for j in range(5):
            io.O[j, i] @= io.I[i, j]
```

Notice that the NDArray values can be indexed using tuples.  The NDArray type
also supports complex slicing patterns, for example:
```python
class Main(m.Circuit):
    io = m.IO(a0=m.Out(m.Array[(4, 5, 3), m.Bit]),
              a1=m.Out(m.Array[(4, 5, 3), m.Bit]),
              b=m.In(m.Array[(4, 5, 2), m.Bit]),
              c=m.In(m.Array[(3, 2), m.Bit]))
    io.a0[0:2] @= io.b
    io.a0[2] @= m.Array[(4, 5), m.Bit]([0 for _ in range(5)])

    io.a1[2, 2:5, 0:2] @= io.c
    io.a1[2, 0:2, 0:2] @= m.Array[(2, 2), m.Bit]([0 for _ in range(2)])
    io.a1[3, :, 0:2] @= m.Array[(5, 2), m.Bit]([0 for _ in range(2)])
    io.a1[0:2, :, 0:2] @= m.Array[(2, 5, 2), m.Bit](
        [m.Array[(2, 5), m.Bit]([0 for _ in range(5)]) for _ in range(2)])
    io.a1[2] @= m.Array[(4, 5), m.Bit]([0 for _ in range(5)])
```

NDArray syntax (tuple type parameter and indexing) is implemented as a simple
layer on top of the base Array type, so NDArrays support all the standard array
syntax and operators (e.g. get_slice and set_slice).


## Valid
Magma provides a built-in `Valid` type parametrized by a type `T` that
constructs a `Product` type with the following fields:
* `valid: Bit`
* `data: T`

Example:
```python
io = m.IO(I=m.In(m.Valid[m.Bits[5]]), valid=m.Out(m.Bit), data=m.Out(m.Bits[5]))
io.valid @= io.I.valid
io.data @= io.I.data
```

## ReadyValid
Magma provides a built-in `ReadyValid` type parametrized by a type `T` that
constructs a `Product` type with the following fields:
* `valid: Bit`
* `data: T`
* `ready: Bit`

The `ReadyValid` type is meant to be used with the type modifiers `Consumer`
and `Producer`.  A `Producer` outputs `valid` and `data` and receives as input
`ready`.  A `Consumer` outputs `ready` and receives as input `valid` and `data.
A handshake occurs when both the `ready` and `valid` signals are high and
indicates that `data` has been transferred from producer to consumer.  These
types are based on the correspond Chisel types.

Here's an example:
```python
io = m.IO(
    I=m.Consumer(T[m.Bits[5]]),
    O=m.Producer(T[m.Bits[5]])
)
# NOTE: inside a circuit definition, the types are flipped, so in this example
# the producer and consumer semantics are viewed from the perspective of the
# client (i.e. the module instancing this module).
io.O.valid @= io.I.valid
io.O.ready @= io.I.ready
io.O.data @= io.I.data
```

The `ReadyValid` type provides some convenience methods:
* `fired()` - Returns a bit that is high when both ready and valid are high.
  Note that for producers this requires `ready` to be driven, and for consumers
  `valid` must be driven.
* `Conumser.enq(data, when=True)` - enqueues the value `data` with an optional
  enable signal (used to drive the valid)
* `Conumser.no_enq(when=True)` - indicates no enqueue should occur with an
  optional condition
* `Producer.deq(when=True)` - deques a value `data` with an option enable
  signal (used to drive ready)
* `Producer.no_deq(when=True)` - indicates no deque should occur with an option
  condition

Magma provides two subclasses of `ReadyValid` with well defined semantics:
* `Decoupled` - `valid` indicates the prdoucer has put valid data in `data`,
  and `ready` indicates that the consumer is ready to accept the data this
  cycle.  No requirements are made on the signaling of ready or valid.
* `Irrevocable` - Promises not to change the value of `data` after a cycle
  where `valid` is high and `ready` is low.  Additionally, once `valid` is
  raised, it will never be lowered until after `ready` has also been raised

Magma also provides two aliases:
* `EnqIO[T]` for `Producer(Decoupled[T])`
* `DeqIO[T]` for `Consumer(Decoupled[T])`

Beyond `Producer` and `Consumer`, `ReadyValid` types support the `In` and
`Monitor` qualifiers which takes a ReadyValid type and returns a view of it
where all the ports are inputs (useful for monitor circuits that want to
observe ready valid transactions).

`ReadyValid` types provide the standard type property `undirected_t` which
returns an undirected version of the type.

`ReadyValid` types do not support the `Out` qualifier.
