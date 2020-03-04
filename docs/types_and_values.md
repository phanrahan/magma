## Magma Types and Values

Magma is a strongly typed language within python.
As in python, all Magma types are python classes.
Instances of Magma types are Magma values.

The first major set of types are single bit types. 
They are subclasses of `Bit`, which itself is a subclass of `Digital`:
```python
class Digital(Type):
  class Bit(Digital):
    class Clock(Bit):
    class Reset(Bit):
    class Enable(Bit):
```
The `Bit` type can be used in logical operations.

The second major type in Magma is the `Array` type.
An `Array` consists of `n` values of the same type `T`.
```python
Array[n, T]
```

The third major type in Magma is the `Tuple` (and `Product`) type.
A `Tuple` consists of `n` unnamed values of different types `Tn`.
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
Bits(n) # ~= Array(n, Bit)
        # &, |, ^, ~, ==, <<, >>
SInt(n) # +, -, *, /, <, <=, >=, >, -, >>>
UInt(n) # +, -, *, /, <, <=, >=, >
```

`Array`, `Tuple`, `Bits`, `UInt`, and `SInt` (Type Constructors) 
are python functions that return new python classes.
Types can be tested for equality and inequality.

Values are instances of Magma type classes.
All values are subclasses of the Magma type `Type`.
