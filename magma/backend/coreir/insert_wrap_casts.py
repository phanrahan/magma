from magma.array import Array
from magma.circuit import Circuit
from magma.clock import AsyncReset, AsyncResetN, Clock, is_clock_or_nested_clock
from magma.conversions import convertbit
from magma.interface import IO
from magma.passes import DefinitionPass, pass_lambda
from magma.t import In, Out, Direction
from magma.tuple import Tuple
from magma.wire import wire


_NAMEDTYPES = (AsyncReset, AsyncResetN, Clock)


class InsertWrapCasts(DefinitionPass):
    def define_wrap(self, wrap_type, in_type, out_type):
        class Wrap(Circuit):
            name = f"coreir_wrap{wrap_type}".replace("(", "").replace(")", "")
            io = IO(**{"in": In(in_type), "out": Out(out_type)})
            coreir_genargs = {"type": wrap_type}
            coreir_name = "wrap"
            coreir_lib = "coreir"
            primitive = True

            def simulate(self, value_store, state_store):
                input_val = value_store.get_value(getattr(self, "in"))
                value_store.set_value(self.out, input_val)
        return Wrap

    def wrap_if_named_type(self, port, definition):
        if isinstance(port, Tuple):
            wrapped = False
            for t in port:
                wrapped |= self.wrap_if_named_type(t, definition)
            return wrapped
        if isinstance(port, Array):
            if not is_clock_or_nested_clock(type(port).T, _NAMEDTYPES):
                return False
            for t in port:
                self.wrap_if_named_type(t, definition)
            return True
        if not port.driven():
            return False
        value = port.value()
        if not isinstance(port, _NAMEDTYPES) or isinstance(value, _NAMEDTYPES):
            return self.wrap_if_named_type(value, definition)
        undirected_t = type(port).qualify(Direction.Undirected)
        if issubclass(type(value), undirected_t):
            return self.wrap_if_named_type(value, definition)
        port_is_clock_type = isinstance(port, (AsyncReset, AsyncResetN, Clock))
        if port_is_clock_type:
            T = Out(type(port))
        else:
            T = In(type(value))

        with definition.open():
            port.unwire(value)
            in_type, out_type = type(port), type(value)
            if not port_is_clock_type:
                # value is the clock type, flip wrap types
                out_type, in_type = in_type, out_type
            inst = self.define_wrap(T, in_type, out_type)()
            wire(convertbit(value, in_type), getattr(inst, "in"))
            wire(inst.out, convertbit(port, out_type))
        return True

    def __call__(self, definition):
        # copy, because wrapping might add instances
        instances = definition.instances[:]
        for instance in instances:
            if type(instance).coreir_name == "wrap" or \
                    type(instance).coreir_name == "unwrap":
                continue
            for port in instance.interface.ports.values():
                self.wrap_if_named_type(port, definition)
        for port in definition.interface.ports.values():
            self.wrap_if_named_type(port, definition)


insert_wrap_casts = pass_lambda(InsertWrapCasts)
