## Circuits and Circuit Instances

The most important class in Magma is the `Circuit` class. 
Circuits roughly correspond to verilog modules.
Circuit instances represent physically realized functional units in hardware.

As an example,
```python
class Mux2(Circuit)
```
represents a basic multiplexer.
By convention, circuit classes are capitalized.

Instancing `Mux2` creates an instance of a multiplexer.
```python
mux2 = Mux2()
```
By convention, circuit instances are named using lower-case.

Often particular circuit classes exist in many differenet
parameterized forms.
Different circuits of that form can be created using a circuit generator.
```python
Mux2x8 = DefineMux(2,8)
```
The function `DefineMux` has two arguments,
the height and the width.
It creates a new circuit class Mux2x8.
But convention, circuit generators begin with the name `Define`.

Circuit instances can then be created using the circuit class.
```python
mux2x8 = Mux2x8()
```

Magma provides many different ways to create circuit instances.
For example,
```python
mux2x8 = Mux(2,8) # equivalent to DefineMux(2,8)()
```
will create a circuit Mux2x8 and then return an instance of that circuit.
The function `Mux` takes the same arguments as `DefineMux`.

It is also possible to create a circuit instance and wire it up immediately.
Assuming `I0:Bits(8)`, `I1:(Bits(8)`, and `S:Bit`,
the following
```python
O = mux(I0, I1, S) # equivalent to Mux(2, len(I0))(I0, I1, S)
```

