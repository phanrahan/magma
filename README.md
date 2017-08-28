# Magma
[![Build Status](https://travis-ci.com/phanrahan/magma.svg?token=BftLM4kSr1QfgPspi6aF&branch=master)](https://travis-ci.com/phanrahan/magma)

Magma is a hardware design language embedded in python.

The central abstraction in Magma is a circuit.
A circuit is a set of functional units that are wired together.
Magma circuits are analagous to verilog modules.
Creating circuits in Magma
is analogous to instantiating modules and wiring them together in verilog.
Thus, all Magma programs are guaranteed to be synthesizable.
Although wiring modules together may seem low-level,
it encourages hardware designers to build reusable components,
similar to how programmers build libraries.

Python is used to to create Magma circuits.
This approach to hardware design using scripting languages
is referred to as *generators* in the hardware community.
Example hardware generators include 
arithmetic units and linear feedback shift registers.
Software engineers more generally 
refer to this technique as *metaprogramming*.
The scripting language is a metaprogram 
in the sense that it is a program that creates a program.

Python has powerful metaprogramming capabilities,
such as decorators and metaclasses.
This makes it possible to create 
higher-level domain-specific languages (DSLs).
Examples include languages for
finite state machines,
memory controllers,
image and signal processing,
and even processors.

The best way to learn Magma is through examples.
Install the system as described below,
and then browse and run the 
jupyter [notebooks](https://github.com/phanrahan/magma/tree/master/notebooks).
Please also refer to the
[documentation](https://github.com/phanrahan/magma/wiki).

The design of Magma was heavily influenced by 
[Chisel](https://chisel.eecs.berkeley.edu/),
so Magma should be easy to learn if you know Chisel.
Magma also has a 
[FIRRTL](https://github.com/freechipsproject/firrtl) backend,
and we hope to demonstrate interoperability with Chisel via FIRRTL soon.

Magma is designed to work with
[Mantle](https://github.com/phanrahan/mantle) 
which contains an extensive a collection of useful circuits;
and with [Loam](https://github.com/phanrahan/loam)
which is used to represent parts and boards,
and to build applications for standalone FPGA boards.

# Installation
## Prerequisites
* python (3 recommended)
* pip
* verilator (for testing)
### MacOS/Homebrew
```
$ brew install python3 verilator
```
### Ubuntu
```
$ sudo apt-get install python3 python3-pip verilator
```


## Setup
Clone the magma repository
```
$ git clone https://github.com/phanrahan/magma
$ cd magma
```

Install the Python dependencies
```
$ pip install -r requirements.txt
```

Install magma as a symbolic package
```
$ pip install -e .
```

Install testing infrastructure and run tests to validate the setup
```
$ pip install pytest
$ pytest tests
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
