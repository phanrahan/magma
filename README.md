Magma is a low-level design language (LLDL) for programming FPGAs.
The central abstraction in Magma is a circuit.
A circuit is a set of functional units 
that are then wired together.
Magma circuits are analagous to structural verilog or netlists.

High-level design languages such as verilog or VHDL 
perform synthesis and behavioral specification of circuits.
Magma takes a different approach.
Synthesis is performed using meta-programming 
using domain-specific languages.
Magma is based on python,
a powerful and widely used programming language.
Python is used to to implement
"generators" that create circuits.
Example generators include 
logic minimiziers,
arithmetic units,
finite state machines,
and even processors.

The second component of the system is Mantle.
Mantle is a library of common hardware components.
Mantle is meant to be like libc or libm.
Mantle primitives are analogous 
to the 7400 series or 4000 series
of discrete integrated circuits.
Typical components include and gates, multiplexers, adders, registers,
shift registers, flip-flops, counters and memories.

Here is a simple Magma program.
```
And2 = And(2)
and2 = And2()

LED(and2(SWITCH[0], SWITCH[1]))
```
And2 is a function that creates 2-bit and gates.
Calling And2 creates a new 2-bit and gate.
And is a high-order function that builds functions
that build and gates of different sizes.
For example, And can be used to create functions 
that create 4-input and gates 
by calling And(4).

Once a circuit for an and gate has been created,
it is connected to some inputs and outputs.
In this example, 
SWITCH[0], SWITCH[1], and LED are also circuits.
Calling and(SWITCH[0], SWITCH[1])
wires SWITCH[0] to the first input of the and gate
and SWITCH[1] to the second input.
Calling LED(and) wires the outout of the and
gate to the input of the LED.

Note that this simple example shows 
how programming hardware is different than software.
In software, there is one version of a function that can
be called from different places in the program.
In hardware, a function represents a circuit.
A new copy of the circuit must be created each time a function is used.
In software, calling a function causes the function to execute.
In hardware, circuits are always executing.
Calling a circuit function 
wires up the arguments to the inputs of the circuit.

Magma currently runs on Xilinx and Lattice ice40 FPGAs.
We use inexpensive FPGA boards such as the Papilio, Mojo, Logi, XULA-2,
and Icestick boards.

More documentation is contained in the doc directory.
Another good place to start is the examples in ```examples```.

