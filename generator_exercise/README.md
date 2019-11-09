# Generator Exercise

In this directory we have several "working" examples of how we could advance magma's notion of generators. In particular there are the following 4 files:
* `current.py`
* `simple_class_generator.py`
* `ergonomic_class_generator.py`
* `holy_grail_class_generator.py`

`common.py` can be ignored as it contains some mock implementations for the various generators. The main purpose of this exercise is to understand what we want to achieve at the user level for writing generators (rather than details of how to implement that.) Each of these files is explained in detail below.

## The problem
Currently, generators in magma are written as standard python functions which return magma circuits (which are python classes). We refer to this as *generators-as-functions*. In this way, generators are *not* a language feature of magma -- rather we achieve that functionality by leveraging the fact that magma is embedded in python, and that we can metaprogram magma using arbitrary python code.

A benefit of this separation is that it is very "easy", both in terms of creating generators (the user can write any python code to create a circuit), and in the language implementation (no extra DSL features are needed to represent generators). Furthermore, the line between host python code and magma DSL code is clear and well-understood.

However, there are limitations to this approach:
* **Lack of structure/formalization:** since generators are just arbitrary python metaprogramming, you can do "anything," which means that consumers of generators have no insight into what a generator function might do. In particular, being able to know the interface of the returned circuit as a function of generator paramaters is useful. For example, we may want to know ahead of time that two different generators have the same mapping from generator parameters to interface. This is not possible using generators-as-functions.
* **Lack of introspection:** As a corollary of the previous point, generators-as-functions do not provide any introspection. They can not provide, in a structured way, extra information about what they do or how they interact with other generators. (You could argue that you can just attach this information as metadata to the function, but the issue is more about providing mechanisms to do this in an intuitive and structured way.)
* **Lack of reuse:** Magma achieves reuse at the circuit level by having the definition -> instance indirection. However, this kind of reuse is not present at the generator level. For example, currently, there is absolutely no relationship between outputs of the same generator with different parameters (e.g. between `Add16` and `Add32`).
The other type of desired reuse is being able to extend/modify existing generators. For example, if you wanted to design a generator which marginally added to an existing generator, it would be productive to reuse the generator logic itself (rather than getting reuse out if its output, which is the current mechanism.)

Later, we also discuss more advanced features which we could potentially build on top of these basic capabilities.

## A path forward
Ideally, we would like to solve these problems, while keeping the benefits of the current generator mechanism (generality and simplicity). After much experimentation, it seems like a pipe-dream, i.e. some trade-offs have to be made. This actually makes sense given the goals; for example, having the generality of arbitrary python metaprogramming *and* formalized generator interfaces is ostensibly dichotomous. Therefore, the remainder of the document discusses the merits of various trade-offs and proposes specific designs in this trade-off space.

### First step: Generators-as-classes
As a first step, moving away from generators-as-functions, and towards *generators-as-classes* provides some of the desired benefits:
* Introspection of generator parameters and values
* Attaching extra information as member functions

### Next step: Improving ergonomics

### Even further: Templated interfaces

## Advanced features
### Parameter inference
### Staging
### Connecting generators
### Propagating parameters
### Editing circuits
