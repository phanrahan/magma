# Magma
[![Documentation Status](https://readthedocs.org/projects/magma/badge/?version=latest)](https://magma.readthedocs.io/en/latest/?badge=latest)
[![Linux Test](https://github.com/phanrahan/magma/actions/workflows/linux-test.yml/badge.svg)](https://github.com/phanrahan/magma/actions/workflows/linux-test.yml)
[![codecov](https://codecov.io/gh/phanrahan/magma/branch/master/graph/badge.svg)](https://codecov.io/gh/phanrahan/magma)
[![Join the chat at https://gitter.im/Magma-HDL/community](https://badges.gitter.im/Magma-HDL/community.svg)](https://gitter.im/Magma-HDL/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

[CHEAT SHEET](https://github.com/phanrahan/magma/blob/master/docs/cheat_sheet.md)

Magma is a hardware design language embedded in python.

The central abstraction in Magma is a circuit.
A circuit is a set of functional units that are wired together.
Magma circuits are analagous to verilog modules.
Thus, all Magma programs are guaranteed to be synthesizable.
Although wiring modules together may seem low-level,
it encourages hardware designers to build reusable components,
similar to how programmers build libraries.

Python is used to to create Magma circuits.
This approach to hardware design using scripting languages
is referred to as *generators* in the hardware community.
Example hardware generators include 
arithmetic units,
linear feedback shift registers,
wallace trees,
and sorting networks.
Software engineers refer to this technique as *metaprogramming*.
The scripting language is a metaprogram 
in the sense that it is a program that creates a hardware program.

In contrast to verilog,
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
The [magma_register_file_tutorial](https://github.com/leonardt/magma_register_file_tutorial)
provides an example of defining and verifying a register file generator.
The
[magmathon](https://github.com/phanrahan/magmathon) repository contains
a set of [Jupyter
Notebooks](https://github.com/phanrahan/magmathon/tree/master/notebooks/tutorial)
that introduce the system. There's also
[magma_examples](https://github.com/leonardt/magma_examples) and
[magma_tutorial](https://github.com/leonardt/magma_tutorial) which contain a
set of basic circuits and tests, providing an example templates for a magma
projects.  Finally there is [magma_riscv_mini](./examples/riscv_mini)
which provides an example of a simple RISCV processor. Please also refer to the
[documentation](http://magma.readthedocs.io/).

The design of Magma was heavily influenced by 
[Chisel](https://chisel.eecs.berkeley.edu/),
so Magma should be easy to learn if you know Chisel.
Some examples from the Chisel tutorial have been ported to
Magma and can be found in [here](https://github.com/leonardt/magma_examples).
Magma also has a 
[FIRRTL](https://github.com/freechipsproject/firrtl) backend,
and we hope to demonstrate interoperability with Chisel via FIRRTL soon.

Magma is designed to work with
[Mantle](https://github.com/phanrahan/mantle) 
which contains an a collection of useful circuits;
and with [Loam](https://github.com/phanrahan/loam)
which is used to represent parts and boards,
and to build applications for standalone FPGA boards.

## Setting up Python
magma requires using Python 3.7+.  This section walks through a few common methods
for getting set up with Python. The first (recommended) method is to use
miniconda which supports MacOS and Linux (and Windows, but magma's support for
windows has not been tested).  We also provide methods using the standard
package managers for MacOS and Ubuntu Linux.

### Universal
[miniconda](https://conda.io/miniconda.html) - A free minimal installer for
conda. Miniconda is a small, bootstrap version of Anaconda that includes only
conda, Python, the packages they depend on and a small number of other useful
packages, including pip, zlib and a few others. Use the conda install command
to install 720+ additional conda packages from the Continuum repository.

Download the installer for your operating system from
[https://conda.io/miniconda.html](https://conda.io/miniconda.html).

The following instructions uses the latest MacOSX release, replace the link in
the wget command for you operating system.
```
$ wget https://repo.continuum.io/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
$ bash Miniconda3-latest-MacOSX-x86_64.sh
# Installing dependencies like matplotlib is typically more reliable with conda than pip
$ conda install matplotlib
```

### MacOS/Homebrew
```
$ brew install python3
```

### Ubuntu
```
$ sudo apt-get install python3 python3-pip
```

### Arch
```
$ pacman -S python python-pip
```

## Installing Dependencies
Magma depends on some third-party libraries that should be installed using your
operating system's package manager.

### MacOS/Homebrew
```
$ brew install verilator gmp mpfr libmpc
```

### Ubuntu
```
$ sudo apt-get install make gcc g++ verilator libgmp-dev libmpfr-dev libmpc-dev
```

## Arch
```
$ pacman -S verilator gmp mpfr libmpc tk
```

## User Setup
Magma is available as a pip package, install the lastest release with:
```
pip install magma-lang
```

## Development Setup
Clone the magma repository
```
$ git clone https://github.com/phanrahan/magma
$ cd magma
```

Install magma as a symbolic package
```
$ pip install -e .
```

Install testing infrastructure and run tests to validate the setup
```
$ pip install pytest  # note that magma requires pytest version 3.3 or later
$ pip install fault 
$ pip install kratos
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
