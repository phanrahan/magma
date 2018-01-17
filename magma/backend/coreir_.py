from collections import OrderedDict
import os
from ..bit import VCC, GND, BitType
from ..array import ArrayKind, ArrayType
from ..clock import wiredefaultclock, ClockType, ResetType
from ..bitutils import seq2int
from ..backend.verilog import find
from ..logging import error
import coreir
from ..ref import ArrayRef, DefnRef
from ..passes import InstanceGraphPass

from collections import defaultdict

class keydefaultdict(defaultdict):
    # From https://stackoverflow.com/questions/2912231/is-there-a-clever-way-to-pass-the-key-to-defaultdicts-default-factory
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError( key )
        else:
            ret = self[key] = self.default_factory(key)
            return ret

def magma_port_to_coreir(port):
    select = repr(port)

    name = port.name
    while isinstance(name, ArrayRef):
        name = name.array.name
    if isinstance(name, DefnRef):
        if name.defn.name != "":
            select = select.replace(name.defn.name, "self")

    return select.replace("[", ".").replace("]", "")

class CoreIRBackend:
    def __init__(self):
        self.context = context = coreir.Context()

        def get_lib(lib):
            if lib in {"coreir", "mantle", "corebit"}:
                return context.get_namespace(lib)
            elif lib == "global":
                return context.global_namespace
            else:
                return context.load_library(lib)
        self.libs = keydefaultdict(get_lib)
        self.__constant_cache = {}
        self.__unique_concat_id = -1

    def check_interface(self, definition):
        # for now only allow Bit or Array(n, Bit)
        for name, port in definition.interface.ports.items():
            if isinstance(port, ArrayKind):
                if not isinstance(port.T, BitKind):
                    error('Error: Argument {} must be a an Array(n,Bit)'.format(port))

    def get_type(self, port, is_input):
        if isinstance(port, (ArrayType, ArrayKind)):
            _type = self.context.Array(port.N, self.get_type(port.T, is_input))
        elif is_input:
            if isinstance(port, ClockType):
                _type = self.context.named_types[("coreir", "clk")]
            elif isinstance(port, ResetType):
                _type = self.context.named_types[("coreir", "rst")]
            else:
                _type = self.context.Bit()
        else:
            if isinstance(port, ClockType):
                _type = self.context.named_types[("coreir", "clkIn")]
            elif isinstance(port, ResetType):
                _type = self.context.named_types[("coreir", "rstIn")]
            else:
                _type = self.context.BitIn()
        return _type

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
            module = lib.modules[name]
            args = {}
            for name, value in instance.kwargs.items():
                if name in {"name", "loc"}:
                    continue  # Skip
                elif isinstance(value, tuple):
                    args[name] = coreir.BitVector(value[1], value[0])
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
                gen_args[name] = value
            gen_args = self.context.new_values(gen_args)
            return module_definition.add_generator_instance(instance.name,
                    generator, gen_args, config_args)

    def add_output_port(self, output_ports, port):
        output_ports[port] = magma_port_to_coreir(port)
        if isinstance(port, ArrayType):
            for bit in port:
                self.add_output_port(output_ports, bit)

    def compile_definition(self, definition):
        self.check_interface(definition)
        module_type = self.convert_interface_to_module_type(definition.interface)
        module = self.context.global_namespace.new_module(definition.coreir_name, module_type)
        module_definition = module.new_definition()
        output_ports = {}
        for name, port in definition.interface.ports.items():
            if port.isoutput():
                self.add_output_port(output_ports, port)

        for instance in definition.instances:
            wiredefaultclock(definition, instance)
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
        for input in definition.interface.inputs():
            output = input.value()
            if not output:
                error(repr(definition))
                raise Exception(f"Output {input} of {definition.name}".format(input))
            self.connect(module_definition, input, output, output_ports)
        module.definition = module_definition
        return module

    def connect(self, module_definition, port, value, output_ports):
        self.__unique_concat_id
        if value is None:
            raise Exception("Got None for port: {}".format(port))
        elif isinstance(value, coreir.Wireable):
            source = value

        elif value.anon() and isinstance(value, ArrayType):
            if os.environ.get("MAGMA_COREIR_FIRRTL", False):
                if not all(isinstance(v, BitType) for v in value):
                    raise NotImplementedError()
                bit_concat_module = self.libs['corebit'].modules["concat"]
                empty_config = self.context.new_values({})
                i = 0
                outputs = []
                for i in range(len(value) - 1, -1, -2):
                    self.__unique_concat_id += 1
                    name = "__magma_backend_concat{}".format(self.__unique_concat_id)
                    module_definition.add_module_instance(name, bit_concat_module, empty_config)
                    module_definition.connect(
                        module_definition.select("{}.in0".format(name)),
                        get_select(value[i]))
                    module_definition.connect(
                        module_definition.select("{}.in1".format(name)),
                        get_select(value[i - 1]))
                    outputs.append(module_definition.select("{}.out".format(name)))
                concat_generator = self.libs['corebit'].generators["concat"]
                width = 2
                while len(outputs) > 1:
                    next_outputs = []
                    config = self.context.new_values({"width0": width, "width1": width})
                    for i in range(0, len(outputs), 2):
                        self.__unique_concat_id += 1
                        name = "__magma_backend_concat{}".format(self.__unique_concat_id)
                        module_definition.add_generator_instance(name, concat_generator, config)
                        module_definition.connect(
                            module_definition.select("{}.in0".format(name)),
                            outputs[i])
                        module_definition.connect(
                            module_definition.select("{}.in1".format(name)),
                            outputs[i + 1])
                        next_outputs.append(module_definition.select("{}.out".format(name)))
                    width *= 2
                    outputs = next_outputs
                source = outputs[0]
            else:
                for p, v in zip(port, value):
                    self.connect(module_definition, p, v, output_ports)
                return
        elif isinstance(value, ArrayType) and all(x in {VCC, GND} for x in value):
            source = self.get_constant_instance(value, len(value),
                    module_definition)
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
                raise NotImplementedError(value)
            if num_bits is None:
                config = self.context.new_values({"value": bool(value)})
                name = "bit_const_{}_{}".format(constant, self.__unique_constant_id)
                corebit_const_module = self.libs['corebit'].modules["const"]
                module_definition.add_module_instance(name, corebit_const_module, config)
            else:
                gen_args = self.context.new_values({"width": num_bits})
                config = self.context.new_values({"value": value})
                name = "const_{}_{}".format(constant, self.__unique_constant_id)
                instantiable = self.get_instantiable("const", "coreir")
                module_definition.add_generator_instance(name, instantiable, gen_args, config)
            return module_definition.select("{}.out".format(name))
            # self.__constant_cache[module_definition][constant] = module_definition.select("{}.out".format(name))
        return self.__constant_cache[module_definition][constant]

    def compile(self, defn):
        modules = {}
        pass_ = InstanceGraphPass(defn)
        pass_.run()
        for key, _ in pass_.tsortedgraph:
            if key.is_definition:
                modules[key.name] = self.compile_definition(key)
        return modules

def compile(main, file_name):
    modules = CoreIRBackend().compile(main)
    modules[main.coreir_name].save_to_file(file_name)
