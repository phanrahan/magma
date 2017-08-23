# Writing Simulation Functions for Primitives

The ```simulate``` function for a primitive is called as a method on the instance
which is being simulated. Therefore the input and output bits of a primitive can be
accessed either through the instance's interface: ```self.interface.ports['I0']```
or simply as an attribute: ```self.I0```. Additionally any initialization parameters
attached to the instance can be accessed through ```self.kwargs```. The simulation function
for a given primitive can be set via setting the ```simulate``` argument for ```DeclareCircuit```
or ```DefineCircuit```.

The simulate function must accept 2 parameters besides ```self```: the value store, which
is an instance of the ```ValueStore``` class, and the state store which is simply a python
dictionary.

The value_store parameter is used to get and set the simulated values of given bits in the
circuit, with ```value_store.get_value(bit)``` and ```value_store.set_value(bit, newval)``` respectively.

```get_value(bit)``` returns the current simulated value of ```bit```. If ```bit``` is an ```ArrayType```, ```get_value```
will return an array of bools for each ```Bit``` in the array, otherwise it will simply return a bool.

```set_value(bit, newval)``` will set bit to a the given new value. ```newval``` must be a bool or an array of bools
if bit is an array.

One implementation detail of the python simulator that needs to be considered is that stateful primitives may be
executed before its inputs are initialized. Therefore in general any stateful primitive's simulation function can
only access its inputs with ```get_value``` when the clock is toggled, otherwise the first execution of the simulation function could access an uninitialized value and the simulator will crash.

The state store parameter begins as an empty python dictionary when simulation starts. This means any simulation
needs to check if the dictionary is empty and then initialize default state values when necessary. For
example, a simulation function for a flip flop may need to store the previous state of the clock in the state store,
and needs to initialize the previous clock value to low when the dictionary is empty.

