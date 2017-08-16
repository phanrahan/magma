from collections import OrderedDict
from magma.backend.verilog import find
from magma.array import ArrayKind, ArrayType
from magma.wire import wiredefaultclock
from magma.bit import VCC, GND
import coreir


class CoreIRBackend:
    def __init__(self):
        self.context = coreir.Context()
        self.libs = {}
        self.unique_instance_id = -1

    def check_interface(self, definition):
        # for now only allow Bit or Array(n, Bit)
        for name, port in definition.interface.ports.items():
            if isinstance(port, ArrayKind):
                if not isinstance(port.T, BitKind):
                    error('Error: Argument {} must be a an Array(n,Bit)'.format(port))

    def convert_interface_to_module_type(self, interface):
        args = {}
        for name, port in interface.ports.items():
            # FIXME: Logic taken from verilog backend, why do we flip?
            if port.isinput(): 
                _type = self.context.Bit()
            elif port.isoutput():
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
            else:
                self.libs[lib] = self.context.load_library(lib)
        instantiable = self.libs[lib].instantiables[name]
        if instantiable.kind == coreir.Module:
            return self.libs[lib].modules[name]
        else:
            return self.libs[lib].generators[name]

    def compile_instance(self, instance, module_definition):
        name = instance.__class__.__name__
        if getattr(instance, 'coreir_lib', False):
            instantiable = self.get_instantiable(name, instance.coreir_lib)
        else:
            len_prefix = len("coreir_")
            assert "coreir_" == name[:len_prefix]
            instantiable = self.get_instantiable(name[len_prefix:], "coreir")
        if isinstance(instantiable, coreir.Module):
            args = {}
            for name, value in instance.kwargs.items():
                args[name] = value[0]  # Drop width for now
            args = self.context.newArgs(args)
            return module_definition.add_module_instance(instance.name, instantiable, args)
        elif isinstance(instantiable, coreir.Generator):
            gen_args = self.context.newArgs({"width": instance.kwargs["WIDTH"]})
            return module_definition.add_generator_instance(instance.name, instantiable, gen_args)
        else:
            raise NotImplementedError()

    def compile_definition(self, definition):
        self.check_interface(definition)
        module_type = self.convert_interface_to_module_type(definition.interface)
        module = self.context.G.new_module(definition.__name__, module_type)
        module_definition = module.new_definition()
        output_ports = {}
        for name, port in definition.interface.ports.items():
            if port.isoutput():
                output_ports[port] = str(port).replace(definition.__name__, "self")
        for instance in definition.instances:
            wiredefaultclock(definition, instance)
            coreir_instance = self.compile_instance(instance, module_definition)
            for name, port in instance.interface.ports.items():
                if port.isoutput():
                    output_ports[port] = str(port)
        for instance in definition.instances:
            for name, port in instance.interface.ports.items():
                if port.isinput():
                    if port.value() is VCC or port.value() is GND:
                        source = self.get_constant_instance(port.value(), module_definition)
                    else:
                        source = module_definition.select(str(output_ports[port.value()]))
                    module_definition.connect(
                        source,
                        module_definition.select(str(port)))
        for input in definition.interface.inputs():
            output = input.value()
            if output:
                module_definition.connect(
                    module_definition.select(str(input).replace(definition.__name__, "self")),
                    module_definition.select(str(output)))
        module.definition = module_definition
        return module

    def get_constant_instance(self, constant, module_definition):
        self.unique_instance_id += 1
        instantiable = self.get_instantiable("const", "coreir")
        if constant == VCC:
            value = 1
        elif constant == GND:
            value = 0
        else:
            raise NotImplementedError
        gen_args = self.context.newArgs({"width": 1})
        config = self.context.newArgs({"value": value})
        name = "const_inst{}".format(self.unique_instance_id)
        module_definition.add_generator_instance(name, instantiable, gen_args, config)
        # FIXME: This should work
        # return instantiable.select("out")
        return module_definition.select("{}.out.0".format(name))

    def compile(self, defn):
        modules = {}
        for key, value in defn.items():
            modules[key] = self.compile_definition(value)
        return modules

def compile(main, file_name):
    defn = find(main, OrderedDict())
    modules = CoreIRBackend().compile(defn)
    modules[main.__name__].save_to_file(file_name)
