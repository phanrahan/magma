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
