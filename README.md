# Magma
[![Build Status](https://travis-ci.com/phanrahan/magma.svg?token=BftLM4kSr1QfgPspi6aF&branch=master)](https://travis-ci.com/phanrahan/magma)

Magma is a low-level language embedded in python.
Currently Magma can be used program FPGAs.
In the future, we hope that Magma will be used
to program CGRAs and ASICs.

The central abstraction in Magma is a circuit.
A circuit is a set of functional units 
that are wired together.
Magma circuits are analagous to verilog modules.
Wiring circuits together creates a netlist.
Thus, all Magma programs are guaranteed to be synthesizable.

Python is used to to create Magma circuits.
This approach to hardware design
is referred to as "generators" in the hardware community,
and "metaprogramming" in the software community.
Example hardware generators include 
logic minimiziers,
arithmetic units,
and linear feedback shift registers.
Using powerful python metaprogramming capabilities
such as decorators and metaclasses makes it possible 
to create higher-level domain-specific languages (DSLs).
Examples include languages for
finite state machines, memory controllers,
image and signal processing, and even processors.

Here is a simple Magma program.
```
And2 = DefineAnd(2)

and2 = And2()

wire( and2(SWITCH[0], SWITCH[1])), LED )
```
In Magma, hardware is built in three stages.
The first stage creates Circuit classes.
Circuits classes when called create circuit instances.
In the above example,
```DefineAnd(n)``` is a parameterized circuit generator
that creates a circuit class that implements an n-bit and gate.
A generator is needed because the class is parameterized.
The second stage creates Circuit instances.
And2 is a Circuit class;
calling And2 creates an instance of a 2-bit and gate.
The third stage wires circuit instances to other circuit instances.
The function call and2(SWITCH[0], SWITCH[1])
wires SWITCH[0] to the first input
and SWITCH[1] to the second input
of the and2 gate.
The output of the and2 gate is returned. and is then wired to the LED.
The function call syntax for wiring 
is equivlanet to explicitly wiring inputs and outputs.
```
# wire( and2(SWITCH[0], SWITCH[1])), LED )
wire( SWITCH[0], and2.I0 )
wire( SWITCH[1], and2.I1 )
wire( and2.O, LED )
```

Note that this Magma example 
shows how programming hardware is different than writing software.
In software, a function is executed sequentially when it is called. 
In hardware, a function is a circuit instance.
A new circuit instance is created each time a function is used.
Each circuit instance represents a different hardware unit
which continuously executing in parallel.

Magma has several backends.
The most commonly used is the coreir backend that
outputs structural verilog 
instancing the coreir intermediste representation primitives.
Included in this relase is also a backend end for the ice40 FPGAs;
this backend uses the open source yosys tool chain for the ice40.
We have also developed  back-ends for Altera and Xilinx FPGAs.

More documentation is contained in the doc directory.
Another good place to start is the examples in ```examples```
and the jupyter notes in ```notebooks```.

