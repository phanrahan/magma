# When Internals
* [Architecture](#architecture)
* [Code](#code)
## Architecture
### Overview
The `when` syntax is designed to provide the ability to perform *conditional*
wiring operations inside a context managed by the Python `with` statement.
This provides magma the ability to overload wiring behavior inside a Python
block without performing a code transformation.  Benefits include interleaving
of native Python `if` statements with magma `when` statements, straightforward
tracebacks for errors (avoids indirection of generated code), and better
performance (avoids parsing/serialization/execution of code).

#### Contexts
Using the when context managers creates an environment where magma's default
wiring behavior changes.  Inside the scope of the context manager, wiring
operations are marked as conditional with respect to the boolean value provided
by the user in the creation of the context.  The when syntax provides a
provides three variants that correspond to standard `if` statement semantics:
`when` (`if`), `elsewhen` (`elif`), and `otherwise` (`else`).  These contexts
can be nested arbitrarily.

If a value is created inside a context (e.g. a module is instanced for an
operator), the value is treated as unconditionally wired unless a nested
context is created.  This allows the user to create instances inside a when
context and have them unconditionally wired, rather than forcing them to create
the instance externally.

#### Validity
The when logic requires that a wire is provided a driver for all the possible
cases of the conditional logic.  That is, if viewed as a traditional `if`
statement, the value must be defined in all branches.  The user may provide a
default driver for a value by wiring the default before entering a conditional
context. Failure to define all possible cases will lead to an inferred latch
error.

#### State
Stateful primitives (`Register` and `Memory`) provide convenience logic for
conditional updates.  By default, these values preserve their state (`Register`
input is the output, `Memory` write enable is inactive).  This is equivalent to
explicitly wiring the relevant ports, which the user may do to make it
explicit, or to override the default behavior.  

For registers, if a user does a conditional wire to a register with an enable,
the enable will be implicitly wired to True, unless the user explicitly wires
it.  The user may override the implicit enable behavior either inside the
context in which the input port is conditionally wired, or externally by, for
example, providing an unconditional driver for the enable.

**TODO** -- Add similar implicit enable logic for memories

#### Introspection
Currently calling introspection methods such as `trace` will return a reference
to an output port of a magma primitive used to contain the when logic.

**TODO** -- We should expose a public API for interacting with `when`
trace/value/etc... (e.g. get a structure mapping conditions to drivers).

#### Metaprogramming
The use of context managers by the `when` syntax enables a form of
metaprogramming that avoids direct syntax manipulation.  Instead, the user may
use standard python code to create `when` contexts programmatically (for
example, inside a loop).  However, with great power comes great responsibility,
for this feature relies on the fact that the `when` context manager pattern is
not checked as native Python syntax, which allows the user to potentially
interleave arbitrary code in between cases of a when statement chain, an
illegal pattern with native Python `if` statements.

### Frontend
#### Context Managers
The `m.when` context manager presents the main entrypoint into the `when` code.
This context manager is used with the Python `with` statement to create a
conditional wiring context.  Wiring statements within the block are conditioned
on the argument passed to the `m.when` constructor.  The `m.elsewhen` and
`m.otherwise` context managers provide the equivalent logic for the `elif` and
`else` cases.
#### Introspection
The user may call `trace` on a conditionally driven value, which will return a
reference to the output of a when primitive instance.
### IR
### Backend

## Code
For various locations in the internal code, this document provides an overview of the
relavant code.
* `array.py/tuple.py`
  * Both recursive types are responsible for providing the
    `set_enclosing_when_context` API, as well as ensuring lazily elaborated children
    inherit the enclosing when context.
* `backend/mlir/mlir_compiler.py`: 
  * `MlirCompiler` calls the `finalize_whens` pass after any passes that may
    modify the circuit are run, and before uniquification (so that when logic
    is elaborated in the repr).  **NOTE:** It could be useful to add a notion
    of dependencies in the pass framework that enforce these constraints (e.g.
    only analysis passes can occur after finalize_whens, no transformation
    passes).
* `backend/mlir/hardware_module.py`
  * `ModuleVisitor` dispatches to `WhenCompiler` when encounter a when
    primitive instance.
* `backend/mlir/when.py`
  * `WhenCompiler`
    * Overview
      * A class encapsulating the MLIR compilation logic for instances of
        the `WhenBuilder` primitive.  It is invoked by the `ModuleVisitor`
        class in `backend/mlir/harware_module.py`.
    * Attributes
      * `_module_visitor`: handle to `ModuleVisitor` instance from
        `backend/mlir/harware_module.py`, used to reference the context for
        creating values, compile options (e.g. `flatten_all_tuples`), and value
        creation helpers (e.g. `make_array_ref`).
      * `_module`: reference to the when primitive MLIR module being compiled
      * `_operands`: reference to `_module.operands`
      * `_flatten_all_tuples`: reference to `flatten_all_tuples` compile option
      * `_outer_block`: get the current active MLIR block, this is used to
        create value references in the enclosing scope, which aims to reduce
        code duplication (since references are cached per block).
      * `_builder`: reference to the magma builder object corresponding to the
        when instance being compiled
      * `_input_to_index`, `_output_to_index`: copies of the builder index maps
        where tuple values are flattened to match the MLIR `flatten_all_tuples`
        logic
      * `_output_wires`: a list of mlir values corresponding to each module
        output
    * Methods
      * `_get_input_index`: retrieve an input magma value's index from the
          `_input_to_index` map
      * `_get_operand`: retrieve the MLIR operand value for a magma value
        (using `_get_input_index` to lookup the position in `_operands`)
      * `_flatten_index_map`: flattens tuples values in  the builder primitive
        index maps to match the MLIR flatten tuples logic
      * `_make_output_wires`: construct the `RegOp` instances for each of the
        module results
      * `_flatten_value`: given a magma value, flatten it into a list of
        children (for flatten all tuples)
      * `_get_parent`: traverse the ancestor chain for an array to see if it's
        contained in the provided index map.  If so, use the index to lookup
        the corresponding MLIR value in the provided collection and return
        a reference to the corresponding array ancestor.  Used to pack
        assignments for an array value.
      * `_check_array_child_wire`: see if a value is a child of an array that is
        in the index map.  If so, return the parent wire and an index
        corresponding to the current child.
      * `_make_operand`: If the operand is an element of wire, emit the
        required array reference ops (extract, get, or slice) to retrieve the desired index.
      * `_build_wire_map`: Collect a map of output wires to their drivers. If
        it's an array that's been elaborated, we collect the drivers in a
        dictionary using their index as a key to sort.
      * `_make_arr_list`: Create a nested list structure matching the
        dimensions of T, used to populate the elements of an array create op.
      * `_build_array_value`: Unpack the contents of value into a nested list
        structure
      * `_combine_array_assign`: Sort drivers by index, use concat or create
        depending on type
      * `_make_assignments`: Use `_build_wire_map` to contruct a mapping from
        output wire to driver.  Use `_build_array_value` and
        `_combine_array_assign` to handle collection elaborated drivers for a
        bulk assign
      * `_process_connections`: given a when block, `_make_assignments` for the
        conditional wires and then process the children
      * `_process_when_block`: If no condition, we are in an otherwise case and
        simply emit the block body (which is inside a previous IfOp).
        Otherwise, we emit an IfOp with the true body corresponding to this
        block, then process the sibilings in the else block
      * `compile`: public API to run the compile logic for a module
* `definition_context.py`: 
  * `DefinitionContext.place_instances` treats when builder's differently
    because they are finalized at a later stage
* `passes/finalize_whens.py`
  * `FinalizeWhens`: when builders are finalized separately than normal
    builders, because the when finalization process should occur after all
    other code that could potentially modify the circuit.  For example, a pass
    could elaborate a value, which would trigger the when resolve logic, which
    needs to occur before the when builder is finalized.
* `primitives/when.py`
  * `iswhen`: public API to check if an instance or definition corresponds to
    the when primitive builder.
  * `InferredLatchError`: raised by latch inference
  * `_add_default_drivers_to_memory_ports`: wires a default zero value to memory
    ports (e.g. waddr and wen are default)
  * `_get_corresponding_register_default`: used to get the default value for
    register inputs (reg.O for reg.I, False for reg.CE)
  * `_add_default_drivers_to_register_inputs`: wires default values for register
    inputs using `_get_corresponding_register_default`
  * `WhenBuilder`
    * Attributes
      * `_block`: corresponding root when block object
      * `_condition_counter`, `_driver_counter`, `_drivee_counter`,
        `_input_counter`, `_output_counter`: counters used to track the number
        of each type of value, which is used to construct a unique name and populate
        their value in the index map.
      * `_input_to_index`, `_output_to_index`: used to look up the corresponding index for
         a value in the MLIR logic
      * `_input_to_name`, `_output_to_name`: used to map a value to the
        corresponding port name
      * `_default_drivers`: used to track the default driver for values
      * `_is_when_builder_`: True (used externally to find when builders)
    * Properties
      * `default_drivers`, `input_to_index`, `output_to_index`, `block`: public
        APIs to internal attributes
    * Methods
      * `_check_existing_derived_ref`: if value is a child of an array or tuple
        that has already been added, we return the child of the existing value,
        rather than adding a new port, which allows us to maintain bulk
        assignments in the eventual generated if statement, rather that
        elaborating into per-child assignments
      * `_generic_add`: common logic for `add_drivee`, `add_driver`, and `add_condition` which
        updates the appropriate maps, adds/gets a corresponding builder port,
        and wires the port to the value
      * `add_drivee`, `add_driver`, `add_condition`: uses `_generic_add` with
        specific maps for each variant
      * `add_default_driver`: adds ports for the driver and drivee, updates the
        `_default_drivers` map
      * `remove_default_driver`: removes drivee from `_default_drivers` map
        (used for unwire)
      * `_finalize`: run latch inference, add default logic for memories and
        registers.
  * `is_when_builder`: public API for checking if instance of when builder

* `protocol_type.py`
  * `Protocol` should pass the `set_enclosing_when_context` API through to the
    underlying magma value
* `util.py`
  * `reset_global_context`, reset the when context global state (used for
    teardown of tests that could potentially error and leave a when context in
    place)
* `when.py`
  * `WhenSyntaxError`: used to report errors about invalid ordering of when
    statements (e.g. an `otherwise` must follow a `when` or `elsewhen`)
  * `ConditionalWire`: a container with fields `drivee` and `driver` used
    to store information about conditional wires
  * `_BlockBase`
    * Overview
      * Base class containing common logic for the various types of when blocks
        (i.e. when, elsewhen, otherwise)
    * Attributes:
      * `self._parent`: for `WhenBlock`, reference to enclosing `WhenBlock` if
        it exists.  For all other blocks, reference to intial `WhenBlock`
      * `self._children`: for `WhenBlock`, reference to child blocks created by
        the `spawn` API
      * `self._conditional_wires`: list of conditional wires created in this block
      * `self._default_drivers`: list of `_default_drivers` for conditional
        values
    * Properties
      * `root`: traverse `_parent` chain until finding the root
      * `condition`: get condition for this block
    * Methods
      * `spawn`: create a child `_WhenBlock`
      * `get_conditional_wires_for_drivee`: return all conditional wires corresponding
        to a drivee
      * `remove_conditional_wire`: remove all conditional wires and the default
        driver for a drivee
      * `add_conditional_wire`: add a conditional wire for an input and an output
      * `new_elsewhen_block`: API to construct an elsewhen block in the chain
      * `new_otherwise_block`: API to construct an otherwise block in the chain
      * `elsewhen_blocks`: get elsewhen blocks
      * `otherwise_blocks`: get otherwise blocks
      * `conditional_wires`: get iterator over `_conditional_wires`
      * `default_drivers`: get generator of `ConditionalWire` objects for
        `_default_drivers` 
      * `get_default_drivers_dict`: get reference to `_default_drivers` dictionary
      * `add_default_driver`: add a new default driver for a drivee
      * `children`: get iterator over `_children`
      * `__enter__`: if needed, add condition to the root builder, push self
        onto block stack
      * `_add_reg_enables`: on exit, add default enable logic for unwired
        registers
      * `_get_exit_block`: returns the block that should be set as the current
        block when __exit__ is called.
      * `__exit__`: add register enables if needed, update the block stack, track
        self as the previous block (used for chaining logic).
  * `get_all_blocks`: given a block, provide a flattened iterator over all the
    child blocks.
  * `_WhenBlockInfo`, `_ElseWhenBlockInfo`: stores the when block condition
  * `_WhenBlock`
    * Overview
      * The `_WhenBlock` corresponds to an invocation of the `when` context
        manager, and tracks the common information for a chain of `elsewhen`
        and `otherwise` blocks.
    * Attributes
      * `_info`: instance of `_WhenBlockInfo` storing condition information
      * `_elsewhens`: list of elsewhen blocks
      * `_otherwise`: otherwise block
      * `_builder`: corresponding builder instance
    * Properties
      * `builder`: public API to `_builder`
      * `root`: return `_parent`'s root if it exists, else return self
      * `condition`: public API to condition information
      * `otherwise_block`: pbulic API to otherwise block
    * Methods
      * `new_elsewhen_block`: public API to create a new elsewhen block
      * `new_otherwise_block`: public API to create a new otherwise block
      * `elsewhen_blocks`: public API to reference `_elsewhen_blocks`
      * `__enter__`: unset previous block in global state to mark the start of
        a fresh when context
      * `_get_exit_block`: return to parent block

  * `_ElseWhenBlock`
    * Overview
      * Specific elsewhen logic that dispatches to its parent `_WhenBlock` for
        common logic
    * Attributes
      * `_info`: instance of `_ElseWhenBlockInfo` storing condition information
    * Properties
      * `root`: always has a parent `_WhenBlock`, return its root
      * `condition`: public API to condition information
      * `otherwise_block`: None, otherwise block is tracked by parent
    * Methods
      * `new_elsewhen_block`: dispatch to parent
      * `new_otherwise_block`: dispatch to parent
      * `elsewhen_blocks`: Empty, elsewhens tracked by parent
      * `_get_exit_block`: dispatch to parent

  * `_OtherwiseBlock`
    * Overview
      * Specific otherwise logic that dispatches to its parent `_WhenBlock` for
        common logic
    * Attributes
      * `_info`: None, no condition
    * Properties
      * `root`: always has a parent `_WhenBlock`, return its root
      * `condition`: None
      * `otherwise_block`: None
    * Methods
      * `new_elsewhen_block`: error, nothing follows an otherwise block.
      * `new_otherwise_block`: error, nothing follows an otherwise block.
      * `elsewhen_blocks`: Empty
      * `_get_exit_block`: dispatch ot parent
  * `_curr_block`, `_prev_block`: global values used to track active and
    previous when contexts
  * `no_when`: temporarily remove active when context
  * `temp_when`: temporarily change active when context
  * `get_curr_block`: get current active when context
  * `_set_curr_block`: set curent active when context
  * `_reset_curr_block`: clear current active when context
  * `_get_prev_block`: get previous active when context
  * `_reset_prev_block`: clear previous active when context
  * `reset_context`: reset current and previous contexts
  * `_get_else_block`: given a block, get the next block in the chain (viewing
    it as nested if/elses)
  * `_get_then_ops`: iterate over conditional wires for current block, then over
    the child blocks
  * `_get_else_ops`: iterate over the next set of ops for an elsewhen or otherwise
  * `_get_assignees_and_latches`: used for latch inferences to track assigned
    values and latched values for a set of ops corresponding to a block
  * `find_inferred_latches`: use `_get_assignees_and_latches` to see if there
    are any latches
  * `when`, `elsewhen`, `otherwise`: public APIs to interact with the when context
    global state to construct corresponding objects tracking the logic


* `wire_container.py`
  * `Wireable`
    * Overview
      * The main `when` logic for the `Wireable` class is to trigger the `when`
        code path when `wire` is invoked inside an active `when` context.  It is
        also responsible for handling unwiring, as well as special logic for
        wiring the output of a when primitive.
    * Attributes:
      * `self._enclosing_when_context`: tracks the active when context when a
        `Wireable` value is created.  This ensures that wiring done inside the
        enclosing context is treated as unconditional.  For example, if we have
        the following code:
        ```python
        with m.when(io.x):
            io.O @= ~io.I
        ```
        the `Invert` instance input port created for the `~` operator should be
        unconditionally wired by `io.I` since it is created inside the context.
      * `self._wire_when_contexts`: tracks the when contexts in which this value
        was wired, which provides faster lookup than having to traverse the
        possible contexts to search for the value.
      * `self._is_when_port`: flag used to track whether a value was create by a
        when builder instance, which enables a special code path for when a when
        output value is directly wired.  This can occur when a user calls
        `.value()` on an conditionally driven value and is returned a handle to
        the when primitive output.
    * Properties
      * `enclosing_when_context`: Set by recursive values (i.e. Tuples and
        Arrays) when constructing child references (i.e. children inherit the
        enclosing context of the parent).
    * Methods
      * `remove_from_wire_when_contexts`: used in the `unwire` logic for
        conditionally driven values
      * `unwire`: has an optional argument `keep_wire_when_contexts` that
        preserves the conditional driver info.  This is used when a value
        is driven by multiple when contexts, where the default value
        may come from a previous when context.  In this case, the value will
        be rewired to new output of the when primitive, but it will maintain
        references to the previous contexts in which it was driven.
      * `_when_output_wire`: Logic responsible for ensuring invariants when
        a user directly wires the output of a when primitive (usually
        referenced by valling `.value()` on a conditionally driven value.).
        This code effectively copies the conditional drivers of the driven
        value and adds them to the same when contexts as drivers for the 
        a value.  This ensures that a when output only drives one value,
        so when a user attempts to wire a when output, we create a new,
        identical when output to drive the target value.
      * `_check_is_when_output`: check if we should use the `_when_output_wire`
        logic.  This logic should be triggered if the value is a when port, or
        the child of a when port.
      * `_wire_impl`: special handling if `self` is a when port
      * `wire`: checks if there is an active when context, if so, trigger
      * conditional wiring logic and add to `self._wire_when_contexts`
  * `AggregateWireable`
    * Overview
      * This extends the `Wireable` code with logic to handle the resolution
        of conditionally driven values.  This ensures that resolved children
        inherit the when logic of the parent.
    * Methods
      * `_get_conditional_drivee_info`: used in the resolve pipeline, collect
        the relevant information related to the when drivers before calling
        `unwire` (at which point the references will be lost)
      * `_rewire_conditional_children`: given the info collected by
        `_get_conditional_drivee_info`, create the corresponding conditional
        wiring for the children
      * `_resolve_conditional_children`: entry point for rewiring the children
        with the appropriate when logic matching the parent being resolved
      * `_resolve_driven_bulk_wire`: check if `_resolve_conditional_children`
        should be called for a conditionally driven value.  If not, the
        children should be wired in the temporary `no_when` context, which is
        important if the parent are being resolved inside an active whe context
        (the children should inherit the parent's lack of `when`, rather than
        the currently active when context)
