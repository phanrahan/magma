## Types of passes:
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
    1. This has a graph which tracks which definitions are dependent on other definitions. Definitions as vertices and instances are directed edges. Each edge points from the definition that uses the instance to the instance's definition.
        1. The graph is stored as a mapping where keys are definitions and values are lists of definitions that the key is dependent on
    1. This inherits DefinitionPass's run, which calls BuildInstanceGraphPass's `__call__` method for each definition (and not for declarations)
    1. The `__call__` hanldes one definition at a time. For each definition, this
        1. Adds the definition to the graph if its not already in there
        2. For each instance in the definition:
            1. Add the instance's definition to the graph if its not already in the graph
            1. Add an edge indicating dependency from the definition using the instance to the instance's definition
    1. tsortedgraph is a list of (definition, `[dependent definitions list]`) sorted so that dependent vertices come after their dependencies
5. InstanceGraphPass -
    1. call BuildInstanceGraphPass to build a dependency graph of definitions for circuit definition passed in as main
    1. set that list as value for self.tsortedgraph
    1. If callable, which it isn't but subclasses might, will call self for each vertex in the sorted graph


## How Are Circuit Definitions And Instances Structured
1. Each definition has a instances list, which is a list of instances in that are added to that definition
2. Each of those instances may have a definition that is gotten by getting the instances type. This is because an instance's definition is the class it is an instance of. Getting the type of an instance gets the class its an instance of.

## Where Do Circuit Declarations, Definitions, and Instances Fit in the Type System? – see [magma/circuit.py](https://github.com/phanrahan/magma/blob/coreir-dev/magma/circuit.py)
1. CircuitKind – instances of this are circuit declarations.
    1. Declarations are like function declarations in C, Magma declarations declare the ports but do not show how to define the circuit. Declarations cannot contain instances. Declarations are used in use cases including wrappers for CoreIR C++ modules that provide definitions, or as an abstract interface for multiple definitions that are backend-dependent.
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

## How do circuit definition/interface interfaces work?
1. Each circuit definition and interface has an interface object.
1. Each Interface instance has a ports dictionary. The dictionary is a mapping of:
    1. key - name of port in interface
    1. value - instance of Magma type, whose name field is a reference to the definition or instance containing this port.
1. The interface of a definition is created in the following way:
    1. The DeclareInterface function is a factory that produces interface. Each interface is a class that is an instance of the InterfaceKind metaclass. This is accomplished because the superclass of InterfaceKind, Kind, is a subclass of type and so calling InterfaceKind's call eventually reaches Kind's `__init__`, which constructs a new Interface type using the type `__init__` function.
    1. When a CircuitDefinition is created, two things happen:
        1. Using CircuitKind's `__new__` method: a new Interface class is created using DeclareInterface.
        1. Using DefineCircuitKind's `__new__` method: an instance of that newly created Interface class is created and assigned to the definition's interface field.
            1. The instance is created by calling the Interface class's `__call__` function, which calls the interface class's constructor. That constructor is _DeclareInterface's `__init__` since the metaclass work used to create the Interface class set _DeclareInterface as its base class.
            1. `_DeclareInterface.__init__` creates a dictionary of ports using this process:
                1. for each port name and port type (where each port type is an instance of the Kind object, and is a type subclassing Type), add a dictionary entry whose key is the name of the port and the value is: an instance of the Type. The Type instance's name field is not actually a name, but is an object holding:
                    1. a reference to the circuit definition or instance containing the port
                    1. the name of the port in the instance



## How does compiling magma circuit definitions to coreir modules work?
1. (optional) – call the compile function that is not part of the CoreIRBackend (CIRB) object. This creates a coreirbackend, calls compile on the coreirbackend with the circuit handed to it
2. Compile for CIRB –
    1. builds a graph of definition -> list of dependent definitions graph using InstanceGraphPass
    1. Call compile_definition for each definition, in order so that higher-order definitions come after the definitions they are dependent on:
        1. check_interface - verifies that the top-level ports on the definition's interface are bits, arrays, or records and that contained types within these ports are also one of those three things.
        1. convert_interface_to_module_definition - create a PyCoreIR record representing the Magma definition's ports. This is done by calling get_type on each ports in the interface of the Magma definition.
            1. get_type takes in a Magma type and converts it and all Magma types contained in it (like bits inside arrays) to PyCoreIR types.
            1. module_type is PyCoreIR type object, specifically a Record
        1. context.global_namespace.new_module - creates a new CoreIR C++ module wrapped by PyCoreIR using python's C interface with the CoreIR C++ library. This module is added to the global CoreIR namespace.
            1. coreir_module is a PyCoreIR module object
        1. coreir_module.new_definition - adds a definition to CoreIR C++ module, returns a pointer to that module wrapped by PyCoreIR's ModuleDef class.
            1. module_definition is a PyCoreIR moduleDef object
        1. compile_definition_to_module_definition -
            1. create a dictionary output_ports using add_output_port:
                1. key - a Magma type instance representing a port (or part of a port) on the Magma definition
                1. values - a string for accesing the port in the CoreIR object
            1. for each instance in the Magma definition:
                1. the wire the clock from definition to the instance if needed
                1. compile_instance - compile it to a PyCoreIR module and add it to the PyCoreIR module definition
                1. add all output ports of the Magma instance to output_ports
            1. for each instance in the Magma definition
                1. connect all input ports to one output port in the PyCoreIR definition using the connect function
                    1. connect -
                        1. arguments are:
                            1. module_definition is the PyCoreIR module definition,
                            1. port is the the type instance for the input magma port
                            1. value is the magma type instance for the output port connected to the input port
                            1. output_ports is the dictionary previously described
                        1. connect recurses until it gets to individual bits, gets the CoreIR select path strings for the input and output ports, and connects them in the PyCoreIR module definition
                        1. Ignore all the extra stuff for things like MAGMA_COREIR_FIRRTL, this is old and dead code
            1. for each port on the interface of the Magma definition
                1. connect it to an output port using the same process as for the input ports of the instances in the definition
        1. assign the created definition to coreir_module and return the module



