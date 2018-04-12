Types of passes:
1. Pass – parent, just takes an object __(I think it’s a circuit, with InstanceGraphPass it’s a circuit, unclear for others)__ and assigns it to the pass’s main
2. InstancePass(Pass) – A pass that finds the paths to all the instances instances in a definition. This includes nested instances (instances which as used in the definitions of other instances).
    1. __init__ - call’s Pass’s init, then creates an empty instances list – main here is a circuit definition
    1. run/_run - BFS search of all instances, return a list of paths to all.
        1. note: callable is meaningless here, since InstancePass never inherited and thus never callable
3. DefinitionPass - A pass that creates a dictionary containing all the definitions used in a top-level circuit definition. It has the names of the definitions as keys and the definition objects as values. The top-level definition is included in the dictionary.
    1. This is a recursive algorithm working on definitions.
        1. It starts with the top level definition (self.main)
        1. For the current iteration's definition, it gets all that definition's instances and recurs on the definition of each instance IF the instance comes from a definition and not a declaration.
            1. Note: variable instancedefinition can contain either definitions or declarations. This is confusing
        1. Add the current iteration's definition to the pass's dictionary of definitions. The self.definitions dictionary has the name of definitions as keys and the definition objects as values.
            1. Note: if the pass is callable, it's called each time a new definition is added to the dictionary.
    1. __is this really what this is doing? Why is this here? Neither DefinitionPass nor InstancePass are ever referenced___
        1. not true. InstancePass never used, but definition pass subclassed a bunch, like BuildInstanceGraphPass.
        2. subclasses of this use DefinitionPass._run to populate the definitions property of the Pass object
    2. __even if this were to do something, shouldn't it need to be changed to call InstancePass to find nested instances?__
        1. No. Since instances can't contain instances, only definitions can, this is not a problem.
    2. __can an instance have a definition in it's instances list? If so, then isn't this pass broken?__ - no, according to circuit.py isdefinition, a circuit is a definition if it has instances. Since can't be both a definition and an instance, instances can't contain instances
        1. definition.instances can only have instances. Instances are instances of either definitions or declarations. These are accessed by type(instance)
    3. __And what does call do? Nothing has a `__call__` method__
        1. The passes that subclass this have `__call__` methods
4. BuildInstanceGraphPass
    1. DefinitionPass gets all the definitions, then calls the `__call__` method on all them (them being the definitions and not the declarations), which builds the graph of
        1. Verticies - the definitions
        2. Edges - the instances.
            1. __what are these edges connecting to? It goes from a vertex (a definition) to what?__
    1. done - makes graph into a list of tuples of (defintion, instances for definition)
5. InstanceGraphPass - call BuildInstanceGraphPass to a tuple of (circuitdefiniton, instances for definition) for all definitions in the cirucit passed in as main, set that list as value for self.tsortedgraph


How Are Circuit Definitions And Instances Structured
1. Each definition has a instances list, which is a list of instances in that are added to that definition
2. Each of those instances may have a definition that is gotten by getting the instances type. This is because an instance's definition is the class it is an instance of. Getting the type of an instance gets the class its an instance of.

Where Do Circuit Declarations, Definitions, and Instances Fit in the Type System? – see [magma/circuit.py](https://github.com/phanrahan/magma/blob/coreir-dev/magma/circuit.py)
1. CircuitKind – instances of this are circuit declarations.
    1. Declarations are like function declarations in C, Magma declarations declare the ports but do not show how to define the circuit. Declarations cannot contain interfaces. Declarations are used in use cases including wrappers for CoreIR C++ modules that provide definitions, or as an abstract interface for multiple definitions that are backend-dependent.
    1. AnonymousCircuitType is an instance of this, __so what does that make instances of AnonymousCircuit? You can’t have instances of a circuit declaration without a definition, right?__
    1. CircuitType is an instance of this, subclass of AnonymousCircuitType
        1. a comment declares instances of CircuitType are instances placed in definitions
    1. DeclareCircuit returns an instance of CircuitKind
        1. __Where is this used differently from the result of DefineCircuit?__
2. DefineCircuitKind – instances of this are circuit definitions. This is a subclass of a CircuitKind.
    1. Defintions are like function definitions in C, they define how a circuit works in hardware, such as the instances of other circuit definitions used inside of the current circuit.
    1. Instances of DefineCircuitKind (known as circuit definitions) get a place method, which allows placing circuit instances in the circuit definitions. Place is called by an instance when the instance is created
        1. Since DefineCircuitKind is used as a metaclass, instances of the circuit definitions don’t get the place method
    1. Circuit is an instance of DefineCircuitKind
        1. CircuitType is Circuit’s parent class,
        1. Circuit – has two functions
            1. Instances of Circuit are circuit instances that are placed in circuit interfaces
            2. Subclasses of circuit are CircuitDefinitions
        1. __Why does Circuit exist? Why not just make CircuitType’s metaclass to be DefineCircuitkind?__
    1. DefineCircuit returns an instance of DefineCircuitKind
3. CircuitType – instances of this are circuit instances that have a declaration and not a definition.
    1. When an instance of CircuitType is created, it’s `__init__` function calls the place of the current active definition, which is stored in the global currentDefinition function
    1. This class (and subclasses of it) are circuit declarations.
4. Circuit - instances of this are circuit instances that have a definition and not a declaration.
    1. This class (and subclasses of it) are circuit definitions.

How does compiling magma circuits (NOT INSTANCES) to coreir modules work?
1. (optional) – call the compile function that is not part of the CoreIRBackend (CIRB) object. This creates a coreirbackend, calls compile on the coreirbackend with the circuit handed to it
2. Compile for CIRB – builds an InstanceGraph using InstanceGraphPass (InstanceGraphPass class in magma.passes.passes)
    1. InstanceGraphPass –
        1. Super is just the pass `__init__`, this just assigns the main property (for storing the main circuit)
        1. BuildInstanceGraphPass -
