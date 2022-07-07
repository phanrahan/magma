# Bind2

`bind2` is the v2 of [bind](../docs/bind.md). The underlying concept represented by `bind2` is the same as `bind` but there are a few key differences.

## Binding to circuits
In order to bind an assertion module to a DUT, call `m.bind2(dut, assertion_module, *bind_arguments)`. It is required that the ports of `dut` are a subset of the ports of `assertion_module` (with the caveat that all ports of `assertion_module` should be inputs, even output ports of `dut`). Note that the only difference between `bind` and `bind2` in this case is the syntax of `dut.bind(assertion_module, *bind_arguments)` vs `m.bind2(dut, assertion_module, *bind_arguments)` respectively.

## Binding to generators
In order to bind an assertion module generator to a DUT generator, call `m.bind2(dut_generator, assertion_module_generator)`. `bind2` requires the following constraints to hold:
* The initializer (i.e. `__init__` method) of `assertion_module_generator` should have the DUT module as its first argument (specifically, this will be an instance of `dut_generator`). For the subsequent arguments, the initializers of `dut_generator` and `assertion_module_generator` should have the same signature, up to default arguments. That is, either they have **exactly** identical signatures, *or* `assertion_module_generator` contains a subset of the arguments of `dut_generator`, and the excluded arguments have default values.
* The interfaces of the instances of `dut_generator` and `assertion_module_generator` when instantiated with the same generator parameters, satisfy the same constraints as the interfaces of `dut` and `assertion_module` respectively, in the circuit binding case. That is, the ports of the `dut_generator` instance should be a subset of the ports of the `assertion_module_generator` instance.
* Each instance of `assertion_module_generator` should either (a) not have any extra bind arguments, or (b) set a special field called `bind2_args` which is a list of the arguments. The length of this list should be exactly the number of extra bind arguments.

## Supported backends.
The CoreIR backend does not support any use of `bind2` (note: it may pass compilation, but will almost certainly not behave as expected).
The MLIR backend fully supports all uses of `bind2`.
