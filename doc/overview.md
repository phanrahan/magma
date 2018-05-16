# The Projects
The projects in order of dependency (with most abstract at top) are:
1. Mantle - libraries of useful circuits built in Magma
1. Magma - A Python API for creating circuits
1. PyCoreIR - A set of Python bindings for manipulating CoreIR data structures.
1. CoreIR - A C++ library for manipulating the CoreIR hardware IR (like LLVM for hardware)

__NOTE: Where does loam fit in here?__

CoreIR can be compiled to verilog to target a diverse array of hardware.

# How Do I Install All These Things?
[See the instructions from this project dependent on all of them](https://github.com/David-Durst/aetherling#installation)

# Core Concepts:
Magma and CoreIR have somewhat similar ways of constructing circuits. There are circuits and types for the values produced and consumed by circuits.

Roughly, the mapping between concepts for circuits in the two platforms is:
1. DeclareCircuit() function that produces a CircuitDeclaration == Generator Declaration + TypeGen
    1. Note; a difference here is that Magma circuit definitions do not require separate declarations, while CoreIR generators do require generator declarations and TypeGens.
1. DefineCircuit() function like DefineUpsample() that produces CircuitDefinitions == Generator
1. CircuitDefinition == Module
1. Instance == Instance

## Magma

### Types
All types inherit from [Type in magma/t.py](https://github.com/phanrahan/magma/blob/master/magma/t.py#L9). Possible types are:
1. Bits (with direction for whether this bit produces or consumes data)
1. Arrays of bits or other types
1. Named tuples of other types

Note that PyCoreIR also has Python implementations of the CoreIR types below. Sometimes you may see these when working with CoreIR objects underlying Magma.

### Circuits
1. CircuitDeclaration - declarations state that a circuit exists and has certain input and ouput wires, but not what the circuit does.
    1. Declarations are like function declarations in C, Magma declarations declare the ports but do not show how to define the circuit.
    1. Declarations cannot contain instances. Declarations are used in use cases including wrappers for CoreIR C++ modules that provide definitions, or as an abstract interface for multiple definitions that are backend-dependent.
    1. Declarations are instances of the CircuitKind class in magma/circuit.py
1. CircuitDefinition -  definitions contain all the properties of declarations as well as an implementation of the circuit to process the input and produce output.
    1. Defintions are like function definitions in C, they define how a circuit works in hardware, such as the instances of other circuit definitions used inside of the current circuit.
    1. Definitions are instances of the DefineCircuitKind class in magma/circuit.py
1. Instances - these are instances of CircuitDefinitions or CircuitDeclarations. You combine multiple instances to implement another circuit definition.

### How To Create And Test A Circuit In Magma?
1. Create a module
1. Implement the module's definition using instances of other modules, like muxes and adders. There are two main ways to do this:
    1. [Aetherling's upsample](https://github.com/David-Durst/aetherling/blob/master/aetherling/modules/upsample.py#L14) shows how to create a circuit definition using a function that creates an instance of a class which inherits from the Circuit class. The returned class is a CircuitDefinition. Calling the CircuitDefinition creates an instance. When DefineUpsampleParallel() is called, an UpsampleParallel circuit definition is returned. Calling that definition creates an instance. The [UpsampleParallel()](https://github.com/David-Durst/aetherling/blob/master/aetherling/modules/upsample.py#L32) function is a shortcut that creates an UpsampleParallel circuit definition, creates an instance of it, and returns only the instance for use in another circuit definition.
        1. Note: The canonical approach when creating a circuit defintion is to create both DefineCircuit() and Circuit() functions (like DefineUpsampleParallel() and UpsampleParallel()) where DefineCircuit() returns a circuit definition and Circuit() calls DefineCircuit() and then returns an instance. This makes it easy to use the circuit in other circuits.
        1. The DefineCircuit() function must always have the @cache_definition annotation to ensure that there is only one instance of each circuit definition with identical parameters. You only want one definition because it is a constructor for producing instances, and there should only be one constructor.
        1. The class must always have two fields:
            1. name - The name of the CircuitDefinition in the magma type system
            1. IO - the input and output ports on the circuit. This is a list that alternates between strings, which are port names, and types, which are the types of the ports. The types should be subclasses of the Type class in magma/t.py.
    1. [Mantle's counter](https://github.com/phanrahan/mantle/blob/master/mantle/common/counter.py#L25) shows how to create a CircuitDefinition using the DefineCircuit() function call. This is an older circuit that provides more flexibility but is more verbose. It is recommended that users do not use it unless necessary.
1. [Aetherling's upsample tests](https://github.com/David-Durst/aetherling/blob/master/tests/test_up.py#L16) show how to take a circuit definition and simulate it using the CoreIR simulator.

## CoreIR

### Types
CoreIR has two type systems:
1. Value Types - These are types of inputs to generators. The full list can be seen [here](https://github.com/rdaly525/coreir/blob/master/include/coreir/ir/valuetype.h) if the below list is out of date:
    1. Bool
    1. Int
    1. BitVector
    1. String
    1. CoreIRType - a generator can be parameterized by a CoreIR type, which can be used to set the type of the inputs of the modules produced by the generator.
    1. Module - a generator can accept a CoreIR module as input.
1. CoreIR Types - These are types of inputs and outputs to circuits. The full list can be seen [here](https://github.com/rdaly525/coreir/blob/master/include/coreir/ir/types.h) if the below list is out of date:
    1. Bit/BitIn/BitInOut - Bit is for outputs. BitIn is for inputs. BitInOut is for ports that do both. InOuts are typically not used.
    1. Arrays of CoreIR types
    1. Records (aka named tuples) of CoreIR types
    1. NamedTypes that alias other CoreIR types, like aliasing a bit for a CE port.

### Circuits
1. Param - an object that defines the parameters to a generator.
    1.
1. TypeGen - an object that defines the types of the modules produced by generators. Multiple generators can have the same typegen.
1. Generator Declarations - a declaration of a generator's name, parameters, and typegen.
1. Generators – functions that produces a module. Parameters to generators should define the structure of the circuit, such as number of inputs or types of variables operated on.
1. Modules - functions that produce instances. Parameters to modules should not change the structure of the circuit. Rather, they should set things like the constant amount that a counter increments by each clock cycle.
1. Instances – a circuit in hardware
    1. Note: in IR, an instance is just a pointer back to a module so that at compilation time, CoreIR knows what to build. This is like LLVM where a call node references a function.

### How To Create And Test A Circuit In CoreIR?
1. Get a namespace to put the generator in. Aetherling shows how to [make a new namespace](https://github.com/rdaly525/coreir/blob/master/src/libs/aetherlinglib.cpp#L19) and [access it for creating things in it](https://github.com/rdaly525/coreir/blob/master/src/libs/aetherlinglib/aeZip2.h#L10).
1. Create a params object. See [Aetherling's Zip2 params object](https://github.com/rdaly525/coreir/blob/master/src/libs/aetherlinglib/aeZip2.h#L18) for an example of how to create one.
1. Create a typegen. See [Aetherling's Zip2 typegen object](https://github.com/rdaly525/coreir/blob/master/src/libs/aetherlinglib/aeZip2.h#L25) for an example.
    1. Note that the record returned by the anonymous function is the type of the modules produced by the generators that use this typegen.
1. Create a generator declaration. See [Aetherling's Zip2 generator](https://github.com/rdaly525/coreir/blob/master/src/libs/aetherlinglib/aeZip2.h#L46) for an example.
1. Add a unit test that just verifies the generator can instantiate modules. This is a basic test that doesn't guarantee correctness. Do this by creating a .cpp file in the tests/unit folder and following [simple.cpp's example](https://github.com/rdaly525/coreir/blob/master/tests/unit/simple.cpp#L6)
1. Add a simulator test that creates a module using instances derived from the generator. This is a complex test that should guarantee correctness. Do this by creating a .cpp file in the tests/simulator folder and following [aetherlingHelpersSim.cpp's example](https://github.com/rdaly525/coreir/blob/master/tests/simulator/aetherlingHelpersSim.cpp).


## How To Interface Between CoreIR and Magma
1. To access CoreIR generators from Magma, use either DefineCircuitFromGeneratorWrapper() or CircuitInstanceFromGeneratorWrapper()
1. To export Magma circuit definitions to CoreIR, use GetCoreIRModule() to get a PyCoreIR module and then call save_to_file("circuitName.json") on that PyCoreIR module to export a CoreIR module as a json file. The json file can be compiled to Verilog using the [CoreIR CLI with the -i flag documented here](https://github.com/rdaly525/coreir/blob/master/doc/StandaloneCoireIR.md#options).

