from magma.array import Array
from magma.circuit import Circuit
from magma.clock import AsyncReset, AsyncResetN, Clock
from magma.conversions import convertbit
from magma.interface import IO
from magma.passes import DefinitionPass, pass_lambda
from magma.t import In, Out, Direction
from magma.tuple import Tuple
from magma.wire import wire


class InsertWrapCasts(DefinitionPass):
    def define_wrap(self, wrap_type, in_type, out_type):
        class Wrap(Circuit):
            name = f"coreir_wrap{wrap_type}".replace("(", "").replace(")", "")
            io = IO(**{"in": In(in_type), "out": Out(out_type)})
            coreir_genargs = {"type": wrap_type}
            coreir_name = "wrap"
            coreir_lib = "coreir"

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
            wrapped = self.wrap_if_named_type(port[0], definition)
            if not wrapped:
                return False
            # TODO: Magma doesn't support length zero array, so slicing a
            # length 1 array off the end doesn't work as expected in normal
            # Python, so we explicilty slice port.ts
            for t in port.ts[1:]:
                self.wrap_if_named_type(t, definition)
            return True
        if not port.driven():
            return False
        value = port.value()
        if not (isinstance(port, (AsyncReset, AsyncResetN, Clock)) or
                isinstance(value, (AsyncReset, AsyncResetN, Clock))):
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
