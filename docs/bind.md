# Bind

`m.bind()` is magma's interface to binding circuits, usually used to bind monitors to design-under-tests (DUTs) for verification.

## Binding to circuits
In order to bind a module to a DUT, call `m.bind(dut, module, *bind_arguments)`. It is required that the ports of `dut` are a subset of the ports of `module` (with the caveat that all ports of `module` should be inputs, even output ports of `dut`). `bind_arguments` contains any extra arguments to `module`'s ports (e.g. XMR's).

## Binding to generators
In order to bind a generator to a DUT, call `m.bind(dut, generator)`. The following constraints hold:
* Both `dut` and `generator` must be subclasses of `m.Generator`.
* The initializer (`__init__()`) of `generator` should have the DUT module as its first argument (specifically, this will be an instance of `dut`). For the subsequent arguments, the initializers of `dut` and `generator` should have the same signature, up to default arguments. That is, either they have **exactly** identical signatures, *or* `generator` contains a subset of the arguments of `dut`, and the excluded arguments have default values.
* The interfaces of the instances of `dut` and `generator` when instantiated with the same generator parameters, satisfy the same constraints as the interfaces of `dut` and `module` in the case of binding circuits. That is, the ports of the `dut` instance should be a subset of the ports of the `generator` instance.
* Each instance of `generator` should either (a) not have any extra bind arguments, or (b) set a special field called `bind_args` (i.e. `self.bind_args = [...]`) which is a list of the arguments. The length of this list should be exactly the number of extra bind arguments.

## Supported backends.
The CoreIR backend does not support any use of `bind` (note: it may pass compilation, but will almost certainly not behave as expected).
The MLIR backend fully supports all uses of `bind`.
