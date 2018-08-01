This directory contains `top.py`, which is an example of implementing an FSM in
magma using a style similar to the Verilog `case` statement.

The state is stored in `mantle.Register` instances and a
`@circuit.combinational` function is used to describe the next state logic.
The output `pixel_valid` is computed as a combinational function of the current
state value.

An equivalent Verilog implementation using `always` blocks can be found in
`top.v`.

`test.py` contains a `fault` test harness that checks both verilog and magma
implementations against the same set of test vectors.
