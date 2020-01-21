from .config import get_debug_mode
from .backend.util import make_relative
from .t import Direction
from .logging import root_logger


__all__  = ['INPUT', 'OUTPUT', 'INOUT']
__all__ += ['flip']
__all__ += ['Port']


INPUT = Direction.In
OUTPUT = Direction.Out
INOUT = Direction.InOut

_logger = root_logger()


def flip(direction):
    assert direction in [INPUT, OUTPUT, INOUT]
    if   direction == INPUT:  return OUTPUT
    elif direction == OUTPUT: return INPUT
    elif direction == INOUT:  return INOUT


def merge_wires(new, old, debug_info):
    oldinputs = set(old.inputs)
    newinputs = set(new.inputs)
    oldoutputs = set(old.outputs)
    newoutputs = set(new.outputs)

    for i in oldinputs - newinputs:
        new.inputs.append(i)
        i.wires = new

    for o in oldoutputs - newoutputs:
        if len(new.outputs) > 0:
            outputs = [o.bit.debug_name for o in new.outputs]
            _logger.error(f"Connecting more than one output ({outputs}) to an "
                          f"input `{i.bit.debug_name}`", debug_info=debug_info)
        new.outputs.append(o)
        o.wires = new


def fast_merge_wires(w, i, o):
    w.inputs = i.wires.inputs + o.wires.inputs
    w.outputs = i.wires.outputs + o.wires.outputs
    w.inputs = list(set(w.inputs))
    w.outputs = list(set(w.outputs))
    if len(w.outputs) > 1:
        outputs = [o.bit.debug_name for o in w.outputs]
        # Use w.inputs[0] as i, similar to {i.bit.debug_name}.
        _logger.error(f"Connecting more than one output ({outputs}) to an "
                      f"input `{w.inputs[0].bit.debug_name}`",
                      debug_info=debug_info)
    for p in w.inputs:
        p.wires = w
    for p in w.outputs:
        p.wires = w


class Wire:
    """
    A Wire has a list of input and output Ports.
    """
    def __init__(self):
        self.inputs = []
        self.outputs = []

    def disconnect(self, o, i):
        self.inputs.remove(i)

    def connect( self, o, i , debug_info):
        """
        Anon Ports are added to the input or output list of this wire.

        Connecting to a non-anonymous port to an anonymous port add the
        non-anonymous port to the wire associated with the anonymous port.
        """

        if not o.anon():
            if o.bit.is_input():
                _logger.error(f"Using `{o.bit.debug_name}` (an input) as an "
                              f"output", debug_info=debug_info)
                return

            if o not in self.outputs:
                if len(self.outputs) != 0:
                    output_str = ", ".join([output.bit.debug_name \
                                            for output in self.outputs])
                    msg = (f"Adding the output `{o.bit.debug_name}` to the "
                           f"wire `{i.bit.debug_name}` which already has "
                           f"output(s) `[{output_str}]`")
                    _logger.warning(msg, debug_info=debug_info)
                self.outputs.append(o)

        if not i.anon():
            if i.bit.is_output():
                _logger.error(f"Using `{i.bit.debug_name}` (an output) as an "
                              f"input", debug_info=debug_info)
                return

            if i not in self.inputs:
                self.inputs.append(i)

        # Always update wires.
        o.wires = self
        i.wires = self

    def check(self):
        for o in self.inputs:
            if o.is_output():
                error("Output in the wire inputs: {}".format(o))

        for o in self.outputs:
            if o.is_input():
                error("Input in the wire outputs: {}".format(o))
                return False

        # Check that this wire is only driven by a single output.
        if len(self.outputs) > 1:
            error("Multiple outputs on a wire: {}".format(self.outputs))
            return False

        return True


class Port:
    """
    Ports implement wiring.

    Each port is represented by a Bit().
    """
    def __init__(self, bit):
        self.bit = bit
        self.wires = Wire()

    def __repr__(self):
        return repr(self.bit)

    def __str__(self):
        return str(self.bit)

    def anon(self):
        return self.bit.anon()

    def unwire(i, o):
        o.wires.disconnect(o, i)
        # Wire can only have one output, so we start with a fresh wire
        i.wires = Wire()

    # wire a port to a port
    def wire(i, o, debug_info):
        """
        Wire a port to a port.
        """
        if i.wires and o.wires and i.wires is not o.wires:
            w = Wire()
            if get_debug_mode():
                merge_wires(w, i.wires, debug_info)
                merge_wires(w, o.wires, debug_info)
            else:
                fast_merge_wires(w, i, o)
        elif o.wires:
            w = o.wires
        elif i.wires:
            w = i.wires
        else:
            w = Wire()

        w.connect(o, i, debug_info)

    def trace(self):
        """
        If the port is an input or inout, return the output.
        If the port is an output, return the first input.
        """
        if not self.wires:
            return None

        if self in self.wires.inputs:
            if len(self.wires.outputs) < 1:
                return None
            assert len(self.wires.outputs) == 1
            return self.wires.outputs[0]

        if self in self.wires.outputs:
            if len(self.wires.inputs) < 1:
                return None
            assert len(self.wires.inputs) == 1
            return self.wires.inputs[0]

        return None

    def value(self):
        """
        If the port is in the inputs, return the output.
        """
        if not self.wires:
            return None

        if self in self.wires.inputs:
            if len(self.wires.outputs) < 1:
                return None
            return self.wires.outputs[0]

        return None

    def driven(self):
        return self.value() is not None

    def wired(self):
        return self.trace() is not None
