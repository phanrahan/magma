Types of passes:
1. Pass – parent, just takes an object (I think it’s a circuit, with InstanceGraphPass it’s a circuit, unclear for others) and assigns it to the pass’s main
2. InstancePass(Pass) – call’s Pass’s init, then creates an empty instances list – main here is a circuit definition
a. run -
i. note: this describes both run and _run
3. DefinitionPass
4. B

Where Do Circuit Declarations, Definitions, and Instances Fit in the Type System? – see magma/circuit.py
1. CircuitKind – instances of this are circuit declarations
    1. AnonymousCircuitType is an instance of this, so what does that make instances of AnonymousCircuit? You can’t have instances of a circuit declaration without a definition, right?
    1. CircuitType is an instance of this, subclass of AnonymousCircuitType
        1. a comment declares instances of CircuitType are instances placed in definitions
    1. DeclareCircuit returns an instance of CircuitKind
        1. Where is this used differently from the result of DefineCircuit?
2. DefineCircuitKind – instances of this are circuit definitions. This is a subclass of a CircuitKind
    1. Instances of DefineCircuitKind (known as circuit definitions) get a place method, which allows placing circuit instances in the circuit definitions. Place is called by an instance when the instance is created
        1. Since DefineCircuitKind is used as a metaclass, instances of the circuit definitions don’t get the place method
    1. Circuit is an instance of DefineCircuitKind
        1. CircuitType is Circuit’s parent class,
        1. Circuit – has two functions
            1. Instances of Circuit are circuit instances that are placed in circuit interfaces
            2. Subclasses of circuit are CircuitDefinitions
        1. Why does Circuit exist? Why not just make CircuitType’s metaclass to be DefineCircuitkind?
    1. DefineCircuit returns an instance of DefineCircuitKind
3. CircuitType – instances of this are circuit instances
    1. When an instance of CircuitType is created, it’s __init__ function calls the place of the current active definition, which is stored in the global currentDefinition function

How does compiling magma circuits (NOT INSTANCES) to coreir modules work?
1. (optional) – call the compile function that is not part of the CoreIRBackend (CIRB) object. This creates a coreirbackend, calls compile on the coreirbackend with the circuit handed to it
2. Compile for CIRB – builds an InstanceGraph using InstanceGraphPass (InstanceGraphPass class in magma.passes.passes)
    1. InstanceGraphPass –
        1. Super is just the pass __init__, this just assigns the main property (for storing the main circuit)
        1. BuildInstanceGraphPass -
