# Uniquification
When assembling and compiling large hardware designs, there are often collisions between names of modules. This issue is especially prominent in the case of using generators, where either the user has to ensure that different generator parameters result in circuits with different names, or the system is responsible for generating unique names. Of course, the latter is desirable.

At the magma level, we can rely on the scoping and lifetime inherent to python to resolve ciruit definitions. That is, if we want to reference a circuit `Foo`, python will resolve `Foo` to the most recently defined circuit with the name `Foo` in the current scope. This part of the resolution comes for free. The issue arises when we want to compile to a backend, e.g. verilog or CoreIR, where scopes are effectively flattened. This document describes the concerns associated with performing uniquification for this purpose and our proposed approach.

## Concerns

### Equality
One of the major components of uniquification is definining the equality operator between two circuits. The desired characteristics of an equality comparator are:
- Fast: it should be fast to determine whether or not two circuits are the same (relative to the rest of the compilation).
- Conservative: the comparator (if not "exact") should never return True if the correct result is False - but can always return False if the correct result is True. That is, false negatives are ok, but false positives are not.

The following are potential implementations of equality operators:
- Node graph isomorphism: This is an undecidable problem is computationally intractable. However, it is the most accurate representation of the true equality operator.
- CoreIR/verilog string comparison: This method is computationally tractable but is bottle-necked by the specific backend compilation flows (which we have found to incur a significant cost). They are also fairly conservative, in that many false negatives are possible. For instance, if instances are re-ordered or renamed, then the circuits will *not* be considered to be equal.
- Circuit characteristics: This method compares a few high-level circuit characteristics, such as the number of instances, the number of outgoing edges for each instance, etc. This method is very fast, and can be done entirely in magma. However, it will likely be more conservative than the CoreIR/verilog string comparison approach.

#### Hashing
On top of any of the above mechanisms, we can apply hashing which would further speed up comparison times, since only hashes would have to be compared not the entire circuit.

### Late vs. Early binding
Another important concern is when uniquification takes place. On one hand, we can perform uniquification at circuit definition time. In implementation, we found this to be easier to perform but if suffers from two major setbacks:
- Uniquification of dynamic circuits: if circuits are not static, i.e. they can be modified after the first time they are defined, then uniquification at definition time is invalid. In particular, if two circuit definitions are found to be equal at definition time, they maybe merged into the same name; however, if they are modified downstream, then this mergning is invalid and the compiled output will also be incorrect.
- Performance: it is possible that circuits which are defined during the course of a program are never actually used during a compilation. Especially when external libraries are imported (e.g. mantle) this can bloat the context and result in a lot more uniquification passes than necessary.

These issues are circumvented if we late-bind the uniquification process. In particular, we propose performing uniquification as a pass at compile time.

## Proposal
We propose the following methodology for uniquification: First, all circuits are attached with a "nominal" name. This is merely a label given to the circuit by the user, but has no semantic meaning. For circuits defined using the `class klass(magma.Circuit)` mechanism, this will be the class name; for circuits defined using `magma.DefineCircuit`, the nominal name will be that which is passed into the `DefineCircuit` function. At the time of circuit definition we do not consider the nominal name; it is effectively metadata.

At compilation time, we perform a pass to change the name of all circuits such that they are unique based on some choice of an equality operator. That is, after this pass, it is guaranteed that any 2 circuits which are not "equal" have different names. Given a single "top", we can perform this pass in toplogical order of dependencies (since circular references are not allowed).
