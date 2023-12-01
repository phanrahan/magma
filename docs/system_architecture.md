# Magma System Architecture

This is a WIP document that aims to capture the key design elements of the
magma system.  Feel free to submit comments using the GitHub issue tracker or
improvements using pull requests.

## Background
### Three Generations of Hardware Design Systems
To better understand the distinction between Magma and related systems, it is
useful to define three distinct classes of hardware design systems that emerged
throughout history.

#### Traditional Hardware Description Languages
Traditional hardware description languages (HDLs) such as Verilog and VHDL
present a syntax for describing hardware that resembles traditional programming
languages such as C.  For example, HDLs provide a fundamental abstraction for
hierarchy called *modules* that bear resemblance to their software counterpart
*functions*, as well as providing a familiar set of operators such as `=, +, -,
...`. While their syntaxes may share many similarities, the essential
differences between HDLs and software languages emerge when inspecting the
language semantics. 

The core semantics of Verilog center around a structural representation that
describes hardware as a hierarchical graph of data flow, computation, and
storage. Components that perform computation (such as logic gates) and store
data (such as register) are connected by wires to describe a circuit.  This
core paradigm most resembles a declarative programming language.

Alongside the structural core, Verilog leverages other language paradigms to
simplify certain aspects of the hardware design process.  This includes
imperative language constructs for describing hardware behavior (such as
`always` blocks), often used for conditional logic and stateful components, and
verification constructs (such as fork/join) used in the creation of testing
infrastructure (often called *test benches*).

One powerful feature provided by modern implementations of Verilog is the
`generate` statement, which enables the use of basic *metaprogramming* to
describe more complex hardware structures.  For example, `generate if` can be
used to conditionally create different hardware structures based on a
parameter, and `generate for` can programmatically generate regular structural
patterns using iteration.  While the `generate` statement greatly increases the
flexibility of hardware descriptions using parameterization techniques, the
power of the language constructs fall short when compared to a standard
programming language.  For example, the `generate` statement cannot employ
recursion, the parameter system does not support objects, and the library
ecosystem pales in comparison to those found for modern programming languages.

#### String Templating Systems
To overcome the limitations of the `generate` statement, sophisticated hardware
designers turned to string templating systems (such as
[Genesis2](https://github.com/StanfordVLSI/Genesis2)) that exposed the full
power of a standard software programming language to the description of
parameterized hardware (often  called *generators*).  This technique enabled
important structural design patterns, such as the ability to parameterize the
ports of module, as well as supporting other aspects of the hardware design
process by providing a single source of truth that not only produced the
logical description of a circuit, but also the collateral for related tasks
including verification, physical design, and firmware development . 

While these systems greatly enhanced the expressiveness of generators, they
lacked essential qualities including safety (strings can be incorrectly
generated and manipulated), introspection (a string of hardware description
language code does not inherently expose information about its contents), and
interoperability (a string describing a hardware object cannot be used by a
library operating on software objects).

#### Hardware Construction Languages
Magma draws significant design inspiration from
[Chisel](https://github.com/chipsalliance/chisel), a modern hardware design
system that coined the term *hardware construction language* (HCL).  Rather
than use strings to represent hardware, HCLs employ an embedded domain-specific
language that capture hardware semantics using native constructs provided by
the host programming language.  Employing an embedding architecture allows the
user to leverage host language features such as introspection for
metaprogramming and libraries for generic programming infrastructure.

Merging the hardware description language into the host programming language
provides an important advantage in the type system.  Rather than have two
distinct type systems (e.g. Perl and Verilog), HCLs share the type system of
the host language, which is typically more powerful than those found in
traditional HDLs.  From a language design and implementation perspective, this
approach avoids duplication of effort (replicating types in both languages),
improves interoperability (consistent types used in both domains), and
acknowledges the large body of work invested in the development of software
type systems.  For example, when embedded in an object-oriented language such
as Python, an HCL automatically leverages features such as inheritance and
polymorphism.  Using a language like Agda would enable an HCL to leverage
dependent typing and theorem proving to guarantee correctness properties of
circuits.

### Magma: Hardware Construction in Python
Magma distinguishes itself from other HCLs by its implementation in Python. The
design of the Python language centers around the principle that *everything is
an object*.  Magma mirrors this object-centric approach in the design of its
hardware abstraction, which makes the HCL easier to learn (aims to be intuitive
to a Python programmer), powerful (provides access to Python's full suite of
metaprogramming facilities), and interoperable (Magma objects can be used with
native Python libraries).  

The choice of alternative host languages, such as Scala for Chisel and Haskell
for Clash, creates a fundamental point of distinction with Magma and in many
cases is the root cause of other differences in the language designs.  For
example, Clash uses a functional abstraction, which sensibly matches the core
abstraction of its Haskell host language.  These host language driven
differences may be reconciled by observing the vibrant ecosystem of software
languages coexisting in practical use today.  Different languages provide
different advantages, and the ability to choose the correct language for the
task at hand improves the quality of life of the user.

While other systems for hardware description exist in Python, such as
[PyMTL](https://github.com/pymtl/pymtl3), Magma differentiates itself in the
details of its embedding architecture.  Magma's design relies heavily on the
Python metaclass system to most effectively capture hardware using idiomatic
Python.  One example is the typing relationship between a Magma `Circuit` (a
class that defines a hardware component) and a `Generator` (a parameterized
class that defines a `Circuit`), achieved by using `Generator` as a metaclass
of `Circuit`.  Magma employs a similar metaclass architecture for its type
system, providing useful relationship between parameterized types and concrete
instances of those types.
