from collections import OrderedDict
from bit_vector import BitVector
import os
from ..bit import VCC, GND, BitType, BitIn, BitOut, MakeBit, BitKind
from ..array import ArrayKind, ArrayType, Array
from ..tuple import TupleKind, TupleType, Tuple
from ..clock import wiredefaultclock, wireclock, ClockType, Clock, ResetType, ClockKind, EnableKind, ResetKind, AsyncResetType, AsyncResetKind
from ..bitutils import seq2int
from ..backend.verilog import find
from ..logging import error
import coreir
from ..ref import ArrayRef, DefnRef, TupleRef
from ..passes import InstanceGraphPass
from ..t import In

from collections import defaultdict

class CoreIRBackendError(RuntimeError):
    pass

class keydefaultdict(defaultdict):
    # From https://stackoverflow.com/questions/2912231/is-there-a-clever-way-to-pass-the-key-to-defaultdicts-default-factory
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError( key )  # pragma: no cover
        else:
            ret = self[key] = self.default_factory(key)
            return ret

def get_top_name(name):
    if isinstance(name, TupleRef):
        return get_top_name(name.tuple.name)
    if isinstance(name, ArrayRef):
        return get_top_name(name.array.name)
    return name

def magma_port_to_coreir(port):
    select = repr(port)

    name = port.name
    name = get_top_name(name)
    if isinstance(name, DefnRef):
        if name.defn.name != "":
            select = select.replace(name.defn.name, "self")

    return select.replace("[", ".").replace("]", "")


magma_coreir_context = coreir.Context()  # Singleton context meant to be used with coreir/magma code
def __reset_context():
    """
    Testing hook so every test has a fresh context
    """
    global magma_coreir_context
    magma_coreir_context = coreir.Context()


class CoreIRBackend:
    def __init__(self, context=None):
        if context is None:
            context = magma_coreir_context
        self.context = context
        self.libs = keydefaultdict(self.context.get_lib)
        self.__constant_cache = {}
        self.__unique_concat_id = -1

    def check_interface(self, definition):
        # for now only allow Bit, Array, or Tuple
        def check_type(port, errorMessage=""):
            if isinstance(port, ArrayKind):
                check_type(port.T, errorMessage.format("Array({}, {})").format(
                    str(port.N), "{}"))
            elif isinstance(port, TupleKind):
                for (k, t) in zip(port.Ks, port.Ts):
                    check_type(t, errorMessage.format("Tuple({}:{})".format(k, "{}")))
            elif isinstance(port, (BitKind, ClockKind, EnableKind, ResetKind, AsyncResetKind)):
                return
            else:
                raise CoreIRBackendError(errorMessage.format(str(port)))
        for name, port in definition.interface.ports.items():
            check_type(type(port), 'Error: Argument {} must be comprised only of Bit, Array, or Tuple')

    def get_type(self, port, is_input):
        if isinstance(port, (ArrayType, ArrayKind)):
            _type = self.context.Array(port.N, self.get_type(port.T, is_input))
        elif isinstance(port, (TupleType, TupleKind)):
            _type = self.context.Record({str(k):self.get_type(t, is_input)
                                         for (k,t) in zip(port.Ks, port.Ts)})
        elif is_input:
            if isinstance(port, ClockType):
                _type = self.context.named_types[("coreir", "clk")]
            elif isinstance(port, AsyncResetType):
                _type = self.context.named_types[("coreir", "arst")]
            else:
                _type = self.context.Bit()
        else:
            if isinstance(port, ClockType):
                _type = self.context.named_types[("coreir", "clkIn")]
            elif isinstance(port, AsyncResetType):
                _type = self.context.named_types[("coreir", "arstIn")]
            else:
                _type = self.context.BitIn()
        return _type

    coreirNamedTypeToPortDict = {
        "clk": Clock,
        "coreir.clkIn": Clock
    }

    def get_ports(self, coreir_type):
        if (coreir_type.kind == "Bit"):
            return BitOut
        elif (coreir_type.kind == "BitIn"):
            return BitIn
        elif (coreir_type.kind == "Array"):
            return Array(len(coreir_type), self.get_ports(coreir_type.element_type))
        elif (coreir_type.kind == "Record"):
            elements = {}
            for item in coreir_type.items():
                # replace  the in port with I as can't reference that
                name = "I" if (item[0] == "in") else item[0]
                elements[name] = self.get_ports(item[1])
                # save the renaming data for later use
                if item[0] == "in":
                    if isinstance(elements[name], BitKind):
                        # making a copy of bit, as don't want to affect all other bits
                        elements[name] = MakeBit(direction=elements[name].direction)
                    elements[name].origPortName = "in"
            return Tuple(**elements)
        elif (coreir_type.kind == "Named"):
            # exception to handle clock types, since other named types not handled
            if coreir_type.name in self.coreirNamedTypeToPortDict:
                return In(self.coreirNamedTypeToPortDict[coreir_type.name])
            else:
                raise NotImplementedError("not all named types supported yet")
        else:
            raise NotImplementedError("Trying to convert unknown coreir type to magma type")

    def get_ports_as_list(self, ports):
        return [item for i in range(ports.N) for item in [ports.Ks[i], ports.Ts[i]]]

    def convert_interface_to_module_type(self, interface):
        args = OrderedDict()
        for name, port in interface.ports.items():
            if not port.isinput() and not port.isoutput():
                raise NotImplementedError()
            args[name] = self.get_type(port, port.isinput())
        return self.context.Record(args)

    def compile_instance(self, instance, module_definition):
        name = instance.__class__.coreir_name
        lib = self.libs[instance.coreir_lib]
        if instance.coreir_genargs is None:
            if hasattr(instance, "wrappedModule"):
                module = instance.wrappedModule
            else:
                module = lib.modules[name]
            args = {}
            for name, value in instance.kwargs.items():
                if name in {"name", "loc"}:
                    continue  # Skip
                elif isinstance(value, tuple):
                    args[name] = BitVector(value[0], num_bits=value[1])
                else:
                    args[name] = value
            args = self.context.new_values(args)
            return module_definition.add_module_instance(instance.name, module, args)
        else:
            generator = lib.generators[name]
            config_args = {}
            for name, value in instance.coreir_configargs.items():
                config_args[name] = value
            config_args = self.context.new_values(config_args)
            gen_args = {}
            for name, value in type(instance).coreir_genargs.items():
                if isinstance(value, AsyncResetKind):
                    value = self.context.named_types["coreir", "arst"]
                gen_args[name] = value
            gen_args = self.context.new_values(gen_args)
            return module_definition.add_generator_instance(instance.name,
                    generator, gen_args, config_args)

    def add_output_port(self, output_ports, port):
        output_ports[port] = magma_port_to_coreir(port)
        if isinstance(port, ArrayType):
            for element in port:
                self.add_output_port(output_ports, element)
        elif isinstance(port, TupleType):
            for element in port:
                self.add_output_port(output_ports, element)

    def compile_declaration(self, declaration):
        # These libraries are already available by default in coreir, so we
        # don't need declarations
        if declaration.coreir_lib in ["coreir", "corebit", "commonlib"]:
            return
        module_type = self.convert_interface_to_module_type(declaration.interface)
        coreir_module = self.context.global_namespace.new_module(declaration.coreir_name, module_type)

    def compile_definition_to_module_definition(self, definition, module_definition):
        output_ports = {}
        for name, port in definition.interface.ports.items():
            if port.isoutput():
                self.add_output_port(output_ports, port)

        for instance in definition.instances:
            wiredefaultclock(definition, instance)
            wireclock(definition, instance)
            coreir_instance = self.compile_instance(instance, module_definition)
            for name, port in instance.interface.ports.items():
                if port.isoutput():
                    self.add_output_port(output_ports, port)


        def get_select(value):
            if value in [VCC, GND]:
                return self.get_constant_instance(value, None, module_definition)
            else:
                return module_definition.select(output_ports[value])

        for instance in definition.instances:
            for name, port in instance.interface.ports.items():
                if port.isinput():
                    self.connect(module_definition, port, port.value(), output_ports)
        for input in definition.interface.inputs(include_clocks=True):
            output = input.value()
            if not output:
                error(repr(definition))
                raise Exception(f"Output {input} of {definition.name} not connected.".format(input))
            self.connect(module_definition, input, output, output_ports)

    def compile_definition(self, definition):
        self.check_interface(definition)
        module_type = self.convert_interface_to_module_type(definition.interface)
        coreir_module = self.context.global_namespace.new_module(definition.coreir_name, module_type)
        module_definition = coreir_module.new_definition()
        self.compile_definition_to_module_definition(definition, module_definition)
        coreir_module.definition = module_definition
        return coreir_module

    def connect(self, module_definition, port, value, output_ports):
        self.__unique_concat_id
        # allow clocks to be unwired as CoreIR can wire them up
        if value is None and isinstance(port, ClockType):
            return
        elif value is None:
            raise Exception("Got None for port: {}, is it connected to anything?".format(port))
        elif isinstance(value, coreir.Wireable):
            source = value

        elif value.anon() and isinstance(value, ArrayType):
            for p, v in zip(port, value):
                self.connect(module_definition, p, v, output_ports)
            return
        elif isinstance(value, ArrayType) and all(x in {VCC, GND} for x in value):
            source = self.get_constant_instance(value, len(value),
                    module_definition)
        elif isinstance(value, TupleType) and value.anon():
            for p, v in zip(port, value):
                self.connect(module_definition, p, v, output_ports)
            return
        elif value is VCC or value is GND:
            source = self.get_constant_instance(value, None, module_definition)
        else:
            source = module_definition.select(output_ports[value])
        module_definition.connect(
            source,
            module_definition.select(magma_port_to_coreir(port)))


    __unique_constant_id = -1
    def get_constant_instance(self, constant, num_bits, module_definition):
        if module_definition not in self.__constant_cache:
            self.__constant_cache[module_definition] = {}
        if constant not in self.__constant_cache[module_definition]:
            self.__unique_constant_id += 1

            bit_type_to_constant_map = {
                GND: 0,
                VCC: 1
            }
            if constant in bit_type_to_constant_map:
                value = bit_type_to_constant_map[constant]
            elif isinstance(constant, ArrayType):
                value = seq2int([bit_type_to_constant_map[x] for x in constant])
            else:
                raise NotImplementedError(constant)
            if num_bits is None:
                config = self.context.new_values({"value": bool(value)})
                name = "bit_const_{}".format(constant)
                corebit_const_module = self.libs['corebit'].modules["const"]
                module_definition.add_module_instance(name, corebit_const_module, config)
            else:
                gen_args = self.context.new_values({"width": num_bits})
                config = self.context.new_values({"value": value})
                # name = "const_{}_{}".format(constant, self.__unique_constant_id)
                name = "const_{}".format(constant)
                instantiable = self.get_instantiable("const", "coreir")
                module_definition.add_generator_instance(name, instantiable, gen_args, config)
            # return module_definition.select("{}.out".format(name))
            self.__constant_cache[module_definition][constant] = module_definition.select("{}.out".format(name))
        return self.__constant_cache[module_definition][constant]

    def compile_dependencies(self, defn):
        modules = {}
        pass_ = InstanceGraphPass(defn)
        pass_.run()
        for key, _ in pass_.tsortedgraph:
            if key == defn:
                continue
            if key.name in modules:
                continue
            if key.is_definition:
                # don't try to compile if already have definition
                if hasattr(key, 'wrappedModule'):
                    modules[key.name] = key.wrappedModule
                else:
                    modules[key.name] = self.compile_definition(key)
                    # key.wrappedModule = modules[key.name]
            else:
                self.compile_declaration(key)
        return modules

    def compile(self, defn):
        modules = self.compile_dependencies(defn)
        if defn.is_definition:
            # don't try to compile if already have definition
            if hasattr(defn, 'wrappedModule'):
                modules[defn.name] = defn.wrappedModule
            else:
                modules[defn.name] = self.compile_definition(defn)
                defn.wrappedModule = modules[defn.name]
        return modules

    def flatten_and_save(self, module, filename, namespaces=["global"], flatten=True, verifyConnectivity=True):
        passes = ["rungenerators", "wireclocks-coreir"]
        if verifyConnectivity:
            passes += ["verifyconnectivity-noclkrst"]
        if flatten:
            passes += ["flattentypes", "flatten"]
        self.context.run_passes(passes, namespaces)
        module.save_to_file(filename)

def compile(main, file_name=None, context=None):
    modules = CoreIRBackend(context).compile(main)
    if file_name is not None:
        return modules[main.coreir_name].save_to_file(file_name)
    else:
        return modules[main.coreir_name]
