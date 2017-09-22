from collections import OrderedDict
from ..bit import VCC, GND
from ..circuit import isdefinition, DefineCircuit, EndDefine
from ..array import ArrayKind, ArrayType
from ..clock import wiredefaultclock, ClockType
from ..bitutils import seq2int
from ..backend.verilog import find
import coreir


class CoreIRBackend:
    def __init__(self, generators):
        self.context = coreir.Context()
        self.libs = {}
        self.generators = generators
        self.__constant_cache = {}

    def check_interface(self, definition):
        # for now only allow Bit or Array(n, Bit)
        for name, port in definition.interface.ports.items():
            if isinstance(port, ArrayKind):
                if not isinstance(port.T, BitKind):
                    error('Error: Argument {} must be a an Array(n,Bit)'.format(port))

    def convert_interface_to_module_type(self, interface):
        args = OrderedDict()
        for name, port in interface.ports.items():
            if port.isinput():
                if isinstance(port, ClockType):
                    _type = self.context.named_types[("coreir", "clk")]
                else:
                    _type = self.context.Bit()
            elif port.isoutput():
                if isinstance(port, ClockType):
                    _type = self.context.named_types[("coreir", "clkIn")]
                else:
                    _type = self.context.BitIn()
            else:
                raise NotImplementedError
            if isinstance(port, ArrayType):
                _type = self.context.Array(port.N, _type)
            args[name] = _type
        return self.context.Record(args)

    def get_instantiable(self, name, lib):
        if lib not in self.libs:
            if lib == "coreir":
                self.libs[lib] = self.context.get_namespace(lib)
            elif lib == "global":
                self.libs[lib] = self.context.global_namespace
            else:
                self.libs[lib] = self.context.load_library(lib)
        instantiable = self.libs[lib].instantiables[name]
        if instantiable.kind == coreir.Module:
            return self.libs[lib].modules[name]
        else:
            return self.libs[lib].generators[name]

    def compile_instance(self, instance, module_definition):
        name = instance.__class__.coreir_name
        if getattr(instance, 'coreir_lib', False):
            instantiable = self.get_instantiable(name, instance.coreir_lib)
        else:
            instantiable = self.get_instantiable(name, "global")
        if isinstance(instantiable, coreir.Module):
            args = {}
            for name, value in instance.kwargs.items():
                args[name] = value[0]  # Drop width for now
            args = self.context.newArgs(args)
            return module_definition.add_module_instance(instance.name, instantiable, args)
        elif isinstance(instantiable, coreir.Generator):
            config_args = {}
            for name, value in instance.coreir_configargs.items():
                config_args[name] = value
            config_args = self.context.newArgs(config_args)
            gen_args = {}
            for name, value in type(instance).coreir_genargs.items():
                gen_args[name] = value
            gen_args = self.context.newArgs(gen_args)
            return module_definition.add_generator_instance(instance.name,
                    instantiable, gen_args, config_args)
        else:
            raise NotImplementedError()

    def get_port_select(self, port, definition):
        select = repr(port)
        if definition.name != "":
            select = select.replace(definition.name, "self")
        return select.replace("[", ".").replace("]", "")

    def compile_definition(self, definition):
        self.check_interface(definition)
        module_type = self.convert_interface_to_module_type(definition.interface)
        module = self.context.global_namespace.new_module(definition.coreir_name, module_type)
        module_definition = module.new_definition()
        output_ports = {}
        for name, port in definition.interface.ports.items():
            if port.isoutput():
                output_ports[port] = self.get_port_select(port, definition)
                if isinstance(port, ArrayType):
                    for bit in port:
                        output_ports[bit] = self.get_port_select(bit, definition)

        for instance in definition.instances:
            wiredefaultclock(definition, instance)
            coreir_instance = self.compile_instance(instance, module_definition)
            for name, port in instance.interface.ports.items():
                if port.isoutput():
                    output_ports[port] = self.get_port_select(port, definition)
                    if isinstance(port, ArrayType):
                        for bit in port:
                            output_ports[bit] = self.get_port_select(bit, definition)


        def connect(port, value):
            if value.anon() and isinstance(value, ArrayType):
                for p, v in zip(port, value):
                    connect(p, v)
                return
            if isinstance(value, ArrayType) and all(x in {VCC, GND} for x in value):
                source = self.get_constant_instance(value, len(value),
                        module_definition)
            elif value is VCC or value is GND:
                source = self.get_constant_instance(value, None, module_definition)
            else:
                source = module_definition.select(output_ports[value])
            module_definition.connect(
                source,
                module_definition.select(self.get_port_select(port, definition)))
        for instance in definition.instances:
            for name, port in instance.interface.ports.items():
                if port.isinput():
                    connect(port, port.value())
        for input in definition.interface.inputs():
            output = input.value()
            assert output, "Output {} not connected".format(input)
            if output.anon():
                assert isinstance(output, ArrayType)
                for i, o in zip(input, output):
                    connect(i, o)
            else:
                connect(input, output)
        module.definition = module_definition
        return module

    def get_constant_instance(self, constant, num_bits, module_definition):
        if module_definition not in self.__constant_cache:
            self.__constant_cache[module_definition] = {}
        if constant not in self.__constant_cache[module_definition]:

            bit_type_to_constant_map = {
                GND: 0,
                VCC: 1
            }
            if constant in bit_type_to_constant_map:
                value = bit_type_to_constant_map[constant]
            elif isinstance(constant, ArrayType):
                value = seq2int([bit_type_to_constant_map[x] for x in constant])
            else:
                raise NotImplementedError(value)
            if num_bits is None:
                config = self.context.newArgs({"value": value})
                name = "bit_const_{}".format(constant)
                instantiable = self.get_instantiable("bitconst", "coreir")
                module_definition.add_module_instance(name, instantiable, config)
            else:
                gen_args = self.context.newArgs({"width": num_bits})
                config = self.context.newArgs({"value": value})
                name = "const_{}".format(constant)
                instantiable = self.get_instantiable("const", "coreir")
                module_definition.add_generator_instance(name, instantiable, gen_args, config)
            self.__constant_cache[module_definition][constant] = module_definition.select("{}.out".format(name))
        return self.__constant_cache[module_definition][constant]

    def get_generator(self, generator):
        for generator_implementation in self.generators:
            if issubclass(generator_implementation, generator):
                return generator_implementation
        raise Exception("Couldn't find generator implementation for "
                "{}".format(generator))

    def compile(self, defn, generators):
        modules = {}
        for name, IO, generator, arguments in generators:
            if name in defn:
                continue
            linked_generator = self.get_generator(generator)
            declaration = linked_generator(*arguments.args, **arguments.kwargs)
            definition = DefineCircuit(name, *IO)
            linked_generator.definition(definition,
                    *arguments.args, **arguments.kwargs)
            EndDefine()
            self.compile_definition(definition)
        for key, value in defn.items():
            modules[key] = self.compile_definition(value)
        return modules


def find_generators(circuit, generators):
    if isdefinition(circuit):
        for i in circuit.instances:
            find_generators(type(i), generators)
    else:
        if hasattr(circuit, '_generator'):
            generators.append((circuit.name, circuit._IO, circuit._generator,
                circuit._generator_arguments))
    return generators


def compile(main, file_name, generators):
    backend = CoreIRBackend(generators)
    defn = find(main, OrderedDict())
    generators = find_generators(main, [])
    modules = backend.compile(defn, generators)
    modules[main.coreir_name].save_to_file(file_name)
