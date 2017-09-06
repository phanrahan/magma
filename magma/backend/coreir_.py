from collections import OrderedDict
from ..bit import VCC, GND
from ..array import ArrayKind, ArrayType
from ..clock import wiredefaultclock, ClockType
from ..bitutils import seq2int
from ..backend.verilog import find
import coreir


class CoreIRBackend:
    def __init__(self):
        self.context = coreir.Context()
        self.libs = {}
        self.__constant_cache = {}

    def check_interface(self, definition):
        # for now only allow Bit or Array(n, Bit)
        for name, port in definition.interface.ports.items():
            if isinstance(port, ArrayKind):
                if not isinstance(port.T, BitKind):
                    error('Error: Argument {} must be a an Array(n,Bit)'.format(port))

    def convert_interface_to_module_type(self, interface):
        args = {}
        for name, port in interface.ports.items():
            if port.isinput(): 
                if isinstance(port, ClockType):
                    _type = self.context.get_named_type("coreir", "clk")
                else:
                    _type = self.context.Bit()
            elif port.isoutput():
                if isinstance(port, ClockType):
                    _type = self.context.get_named_type("coreir", "clkIn")
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
                self.libs[lib] = self.context.G
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
        elif "coreir_" in name:
            len_prefix = len("coreir_")
            assert "coreir_" == name[:len_prefix]
            instantiable = self.get_instantiable(name[len_prefix:], "coreir")
        else:
            instantiable = self.get_instantiable(name, "global")
        if isinstance(instantiable, coreir.Module):
            args = {}
            for name, value in instance.kwargs.items():
                args[name] = value[0]  # Drop width for now
            args = self.context.newArgs(args)
            return module_definition.add_module_instance(instance.name, instantiable, args)
        elif isinstance(instantiable, coreir.Generator):
            gen_args = self.context.newArgs({"width": instance.kwargs["width"]})
            return module_definition.add_generator_instance(instance.name, instantiable, gen_args)
        else:
            raise NotImplementedError()

    def compile_definition(self, definition):
        self.check_interface(definition)
        module_type = self.convert_interface_to_module_type(definition.interface)
        module = self.context.G.new_module(definition.coreir_name, module_type)
        module_definition = module.new_definition()
        output_ports = {}
        for name, port in definition.interface.ports.items():
            if port.isoutput():
                output_ports[port] = repr(port).replace(definition.coreir_name, "self")
                if isinstance(port, ArrayType):
                    for bit in port:
                        output_ports[bit] = repr(bit).replace("[", ".").replace("]", "").replace(definition.coreir_name, "self")

        for instance in definition.instances:
            wiredefaultclock(definition, instance)
            coreir_instance = self.compile_instance(instance, module_definition)
            for name, port in instance.interface.ports.items():
                if port.isoutput():
                    output_ports[port] = repr(port)
                    if isinstance(port, ArrayType):
                        for bit in port:
                            output_ports[bit] = repr(bit).replace("[", ".").replace("]", "")


        def connect(port, value):
            if value.anon() and isinstance(value, ArrayType):
                for i, v in zip(range(len(port)), value):
                    connect("{}.{}".format(repr(port), i), v)
                return
            if isinstance(value, ArrayType) and all(x in {VCC, GND} for x in value):
                source = self.get_constant_instance(value, len(value),
                        module_definition)
            elif value is VCC or value is GND:
                source = self.get_constant_instance(value, 1, module_definition)
            else:
                source = module_definition.select(output_ports[value])
            module_definition.connect(
                source,
                module_definition.select(repr(port).replace(definition.coreir_name, "self")))
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
                    module_definition.connect(
                        module_definition.select(repr(i).replace(definition.coreir_name, "self").replace("[", ".").replace("]", "")),
                        module_definition.select(repr(o)))
            else:
                module_definition.connect(
                    module_definition.select(repr(input).replace(definition.coreir_name, "self")),
                    module_definition.select(repr(output)))
        module.definition = module_definition
        return module

    def get_constant_instance(self, constant, num_bits, module_definition):
        if constant not in self.__constant_cache:
            instantiable = self.get_instantiable("const", "coreir")

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
            gen_args = self.context.newArgs({"width": 1})
            config = self.context.newArgs({"value": value})
            name = "const_{}".format(constant)
            module_definition.add_generator_instance(name, instantiable, gen_args, config)
            self.__constant_cache[constant] = module_definition.select("{}.out".format(name))
        return self.__constant_cache[constant]

    def compile(self, defn):
        modules = {}
        for key, value in defn.items():
            modules[key] = self.compile_definition(value)
        return modules

def compile(main, file_name):
    defn = find(main, OrderedDict())
    modules = CoreIRBackend().compile(defn)
    modules[main.coreir_name].save_to_file(file_name)
