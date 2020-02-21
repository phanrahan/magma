## Circuit Declarations

Circuit declarations are used to declare primitive built-in circuits.
The most common use for a circuit declaration is to declare a built-in verilog module.

The function
```python
C = DeclareCircuit( name, typesignature )
```
returns a class which is a subclass of `Circuit`.
This circuit can be instanced.
The type signature has the form `(name0, type0, name1, type1, ..., namen, typen)`
The types should be qualified as inputs or outputs.

For example,
```python
SB_LUT4 = DeclareCircuit('SB_LUT4',
               "I0", In(Bit),
               "I1", In(Bit),
               "I2", In(Bit),
               "I3", In(Bit),
               "O",  Out(Bit))
```
declares the Silicon Blue LUT4 primitive
that is built-in to the Lattice ice40 and yosys verilog compilers.
This primitive has 4 inputs each declared as `In(Bit)`,
and a single output declared as `Out(Bit)`.

To create `lut4` circuit instance on the FPGA, we instance `SB_LUT4`.
```python
lut4 = SB_LUT4(LUT_INIT=0xffff)
```
Here we pass in the 16-bit value which is used to initialize the LUT.

## Circuit Definitions

it is easy to add new circuit classes to Magma
using circuit definitions.

For example,
```python
FA = DefineCircuit('FullAdder', 'a', In(Bit), 'b', In(Bit), 'cin', In(Bit), 's', Out(Bit), 'co', Out(Bit))
s = FA.a ^ FA.b ^ FA.cin
wire(s, FA.s)
cout = (FA.a & FA.b) | (FA.b & FA.cin) | (FA.a & FA.cin)
wire(cout, FA.cout)
EndCircuit()
```
`FA` is a subclass of `Circuit`. 
It has been enhanced to include the arguments in the function signature,
in this case the inputs `a`, `b`, `cin` and the outputs `s` and `cout`.
Inside the circuit definition we can instance circuits and wire them together.

Once `FA` has been defined, we can create circuit instances from it
```python
fa = FA()
```

`DefineCircuit` has the same function signature as `DeclareCircuit`.
```python
C = DefineCircuit( name, typesignature )
```
`EndCircuit` is needed to end the current circuit definition.
Note that it is possible to nest circuit definitions.

Note that circuit definitions are cached using the name of the circuit. 
Defining a circuit a second time with the same name returns the same circuit class.

## Circuit subclasses

The recommended way to create new circuits is to subclass Circuit.
```python
class FullAdder(Circuit):
    name = "FullAdder"
    IO = ["a", In(Bit), "b", In(Bit), "cin", In(Bit), "s", Out(Bit), "cout", Out(Bit)]
    @classmethod
    def definition(io):
        # Generate the sum
        s = io.a ^ io.b ^ io.cin
        wire(s, io.s)
        # Generate the carry
        cout = (io.a & io.b) | (io.b & io.cin) | (io.a & io.cin)
        wire(cout, io.cout)
```
The circuit signature is contained in the attributes of `FullAdder`,
in particular, `name` and `IO`.
The actual definition is inside the method `definition`.
Note that this is a class method.
Note also that the circuit being defined is passed as an argument to `definition`,
and the body of that function is identical to the code inside `DefineCircuit` and `EndCircuit`.

This magic is all done with python metaclasses.

## Verilog

It is useful to be able to declare circuits from verilog source.

We provide two utilities for doing this.
```python
modules = declare_from_verilog(source)
modules = declare_from_verilog_file(filename)
```
These functions return a list of Circuits, one for each module in the verilog file.
The circuits will have the same name and interface as the modules in the verilog file.
The verilog file is parsed using the python module `pyverilog`,
which must be installed.

Here is a simple example,
```python
from magma import declare_from_verilog

source = '''\
module CSA4 ( input [3:0] a,b,c, output [3:0] s, co);
   assign s = a ^ b ^c;
   assign co = a&b | b&c | a&c;
endmodule'''

CSA4 = declare_from_verilog(source)[0]
```

Another useful technique is to run a text templating engine over the verilog file before parsing.
```python
modules = DefineFromTemplatedVerilog(template, **kwargs)
modules = DefineFromTemplatedVerilogFile(templatefilename, **kwargs)
```
We use the `mako` templating engine.
The arguments `kwargs` appear in the global name space of the python code in the template.
These functions return a list of Circuits, one for each module in the verilog file.
The circuits will have the same name and interface as the modules in the verilog file.

```python
from magma import DefineFromTemplatedVerilog

source = '''\
module CSA${N} ( input [${N-1}:0] a,b,c, output [${N-1}:0] s, co );
   assign s = a ^ b ^c;
   assign co = a&b | b&c | a&c;
endmodule'''

CSA4 = DefineFromTemplatedVerilog(source, **dict(N=4))[0]
```

Examples using these two functions are in a [jupyter
notebook](https://github.com/phanrahan/magmathon/blob/master/notebooks/advanced/verilog.ipynb)
