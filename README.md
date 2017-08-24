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


# Installation
## Prerequisites
* python (3 recommended)
* pip
### MacOS/Homebrew
```
$ brew install python3
```
### Ubuntu
```
$ sudo apt-get install python3 python3-pip
```

## Setup
**NOTE:** instructions assume Python 3 has been installed. On Ubuntu and
MacOs/Homebrew that means `pip3` will be the package manager.

Install the Python dependencies
```
$ pip3 install -r requirements.txt
```

Install magma as a symbolic package
```
$ pip3 install -e .
```

Install testing infrastructure and run tests to validate the setup
```
$ pip3 install pytest
$ pytest
```

You should see something like
```
============================= test session starts ==============================
platform darwin -- Python 3.6.1, pytest-3.0.7, py-1.4.33, pluggy-0.4.0
rootdir: ..../repos/magmacore, inifile:
collected 70 items

tests/test_circuit/test_anon.py .
tests/test_circuit/test_declare.py .
tests/test_circuit/test_define.py .
tests/test_higher/test_braid.py .
tests/test_higher/test_curry.py .
tests/test_higher/test_currylut.py .
tests/test_higher/test_curryrom.py .
tests/test_higher/test_flat.py .
tests/test_higher/test_fork.py .
tests/test_higher/test_higher_compose.py .
tests/test_higher/test_join.py .
tests/test_interface/test_interface.py ....
tests/test_io/test_inout1.py .
tests/test_io/test_inout2.py .
tests/test_io/test_out1.py .
tests/test_io/test_out2.py .
tests/test_ir/test_declaretest.py .
tests/test_ir/test_ir.py .
tests/test_meta/test_class.py .
tests/test_meta/test_creg.py .
tests/test_simulator/test_counter.py .
tests/test_simulator/test_ff.py .
tests/test_simulator/test_logic.py .
tests/test_type/test_anon_type.py .
tests/test_type/test_array.py .
tests/test_type/test_array2d.py .
tests/test_type/test_arrayconstruct.py .
tests/test_type/test_arrayflip.py .
tests/test_type/test_arrayval.py .
tests/test_type/test_awire1.py .
tests/test_type/test_bit.py .
tests/test_type/test_bitflip.py .
tests/test_type/test_bitval.py .
tests/test_type/test_tuple.py .
tests/test_type/test_tupleconstruct.py .
tests/test_type/test_tupleflip.py .
tests/test_type/test_tupleval.py .
tests/test_type/test_twire1.py .
tests/test_type/test_type_errors.py ...
tests/test_type/test_vcc.py .
tests/test_type/test_whole.py .
tests/test_type/test_wire1.py .
tests/test_type/test_wire2.py .
tests/test_type/test_wire3.py .
tests/test_type/test_wire4.py .
tests/test_type/test_wire5.py .
tests/test_verilog/test_verilog.py .
tests/test_wire/test_arg1.py .
tests/test_wire/test_arg2.py .
tests/test_wire/test_array1.py .
tests/test_wire/test_array2.py .
tests/test_wire/test_array3.py .
tests/test_wire/test_call1.py .
tests/test_wire/test_call2.py .
tests/test_wire/test_compose.py .
tests/test_wire/test_const0.py .
tests/test_wire/test_const1.py .
tests/test_wire/test_errors.py ..
tests/test_wire/test_flip.py .
tests/test_wire/test_named1.py .
tests/test_wire/test_named2a.py .
tests/test_wire/test_named2b.py .
tests/test_wire/test_named2c.py .
tests/test_wire/test_pos.py .

========================== 70 passed in 1.45 seconds ===========================
```
