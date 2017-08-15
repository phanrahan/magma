from collections import OrderedDict
from magma.backend.verilog import find
from magma.array import ArrayKind, ArrayType
from magma.wire import wiredefaultclock
import coreir


class CoreIRBackend:
    def __init__(self):
        self.context = coreir.Context()
        self.coreir_stdlib = self.context.get_namespace("coreir")

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

    def compile_instance(self, instance, module_definition):
        # for key, value in instance.interface.ports.items():
        #     if value.isinput():
        #         # Find the output connected to value
        name = instance.__class__.__name__
        len_prefix = len("coreir_")
        assert "coreir_" == name[:len_prefix]
        instantiable = self.coreir_stdlib.instantiables[name[len_prefix:]]
        if instantiable.kind == coreir.Module:
            return module_definition.add_module_instance(instance.name, instantiable)
        elif instantiable.kind == coreir.Generator:
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
                    module_definition.connect(
                        module_definition.select(str(output_ports[port.value()])),
                        module_definition.select(str(port)))
        module.definition = module_definition
        return module

    def compile(self, defn):
        modules = {}
        for key, value in defn.items():
            print('compiling', key)
            modules[key] = self.compile_definition(value)
        return modules

def compile(main, file_name):
    defn = find(main, OrderedDict())
    modules = CoreIRBackend().compile(defn)
    modules[main.__name__].save_to_file(file_name)
