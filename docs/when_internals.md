# When Internals

For various locations in the internal code, this document provides an overview of the
relavant code.

* `wire_container.py`
  * `Wireable`
    * Overview
      *
    * Attributes:
      * `self._enclsoing_when_context`: tracks the active when context when a
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

