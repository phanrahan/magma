# Migrating to magma 2

* Operator definitions (e.g. `+`, `-`, ...) have moved from mantle to magma.
  This should not cause any user facing code changes, but the names of
  generated circuits may be different.  It also means that coreir primitives
  will always be used to implement the operators (before, it would dispatch to
  the current mantle target).  Support for other mantle targets will be added
  later as implementations of the coreir primitives.
* Rename `<..>Type` to `<...>`. No more type constructors (e.g. `ArrayType`
  becomes `Array`).  Parametrized types are constructed using the bracket
  syntax (e.g. `Array[5, Bit]`)
* `isinstance(..., <...>Kind)`  -> `issubclass(..., <...>)`. Concrete
  parameterized types are subclasses of the abstract type) (e.g. `isinstance(T,
  BitsKind)` becomes `issubclass(T, Bits)`
* `_Bit` -> `Digital`. Renamed parent type of Bit, Clock, Reset, ...
* `Tuple(...)` -> `Product.from_fields("anon", dict(...))`. Tuple now refers to
  a heterogenous type indexed by position (e.g. x[0], x[1], ...), while Product
  is used for the key/value version (e.g. x.a, x.y, ...).  Magma previously
  used Tuple to represent both versions.  This change is in line with the
  `hwtypes` `Tuple` and `Product` types (as well as Python's `tuple` vs
  `namedtuple`). `"anon"` is the name of the type (before all magma tuples
  were "anonymous").  We are considering an interface for declaring
  anonymous Products so the user does not have to supply a name.
* `<Tuple>.Ks` -> `<Tuple>.keys()` and `<Tuple>.Ts` -> `<Tuple>.types()` these
  attributes were refactored to methods to be more clear/consistent with the
  hwtypes tuple.
* `isinput`, `isinout`, `isoutput` renamed to `is_input`, `is_inout`,
  `is_output` for clarity


See these PRs for examples of these changes
* Mantle: https://github.com/phanrahan/mantle/pull/165
* Fault: https://github.com/leonardt/fault/pull/187
