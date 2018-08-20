from .logging import error, warning, get_source_line
from .backend.util import make_relative
from .ref import DefnRef, InstRef

__all__  = ['INPUT', 'OUTPUT', 'INOUT']
__all__ += ['flip']
__all__ += ['Port']

INPUT = 'input'
OUTPUT = 'output'
INOUT = 'inout'


def report_wiring_error(message, debug_info):
    error(f"\033[1m{make_relative(debug_info[0])}:{debug_info[1]}: {message}",
          include_wire_traceback=True)
    error(get_source_line(debug_info[0], debug_info[1]))


def flip(direction):
    assert direction in [INPUT, OUTPUT, INOUT]
    if   direction == INPUT:  return OUTPUT
    elif direction == OUTPUT: return INPUT
    elif direction == INOUT:  return INOUT

def mergewires(new, old):
    oldinputs = set(old.inputs)
    newinputs = set(new.inputs)
    oldoutputs = set(old.outputs)
    newoutputs = set(new.outputs)

    for i in oldinputs - newinputs:
        new.inputs.append(i)
        i.wires = new

    for o in oldoutputs - newoutputs:
        if len(new.outputs) > 0:
            error("Connecting more than one output to an input {}".format(o), include_wire_traceback=True)
        new.outputs.append(o)
        o.wires = new


#
# A Wire has a list of input and output Ports.
#
class Wire:
    def __init__(self):
        self.inputs = []
        self.outputs = []

    def connect( self, o, i , debug_info):

        # anon Ports are added to the input or output list of this wire
        #
        # connecting to a non-anonymous port to an anonymous port
        # add the non-anonymous port to the wire associated with the
        # anonymous port

        #print(str(o), o.anon(), o.bit.isinput(), o.bit.isoutput())
        #print(str(i), i.anon(), i.bit.isinput(), i.bit.isoutput())

        if not o.anon():
            #assert o.bit.direction is not None
            if o.bit.isinput():
                report_wiring_error(f"Using {o.bit.debug_name} (an input) as an output", debug_info)
                return

            if o not in self.outputs:
                if len(self.outputs) != 0:
                    warning("Warning: adding an output {} to a wire with an output {}".format(str(o), str(self.outputs[0])))
                #print('adding output', o)
                self.outputs.append(o)

        if not i.anon():
            #assert i.bit.direction is not None
            if i.bit.isoutput():
                report_wiring_error(f"Using {i.bit.debug_name} (an output) as an input", debug_info)
                return

            if i not in self.inputs:
                #print('adding input', i)
                self.inputs.append(i)

        # print(o.wires,i.wires,self,self.outputs,self.inputs)

        # always update wires
        o.wires = self
        i.wires = self

    def check(self):
        for o in self.inputs:
            if o.isoutput():
                error("Output in the wire inputs: {}".format(o))

        for o in self.outputs:
            if o.isinput():
                error("Input in the wire outputs: {}".format(o))
                return False

        # check that this wire is only driven by a single output
        if len(self.outputs) > 1:
            error("Multiple outputs on a wire: {}".format(self.outputs))
            return False

        return True

#
# Port implements wiring
#
# Each port is represented by a Bit()
#
class Port:
    def __init__(self, bit):

        self.bit = bit

        self.wires = Wire()

    def __repr__(self):
        return repr(self.bit)

    def __str__(self):
        return str(self.bit)

    def anon(self):
        return self.bit.anon()

    # wire a port to a port
    def wire(i, o, debug_info):
        #if o.bit.direction is None:
        #    o.bit.direction = OUTPUT
        #if i.bit.direction is None:
        #    i.bit.direction = INPUT

        #print("Wiring", o.bit.direction, str(o), "->", i.bit.direction, str(i))

        if i.wires and o.wires and i.wires is not o.wires:
            # print('merging', i.wires.inputs, i.wires.outputs)
            # print('merging', o.wires.inputs, o.wires.outputs)
            w = Wire()
            mergewires(w, i.wires)
            mergewires(w, o.wires)
            # print('after merge', w.inputs, w.outputs)
        elif o.wires:
            w = o.wires
        elif i.wires:
            w = i.wires
        else:
            w = Wire()

        w.connect(o, i, debug_info)

        #print("after",o,"->",i, w)


    # if the port is an input or inout, return the output
    # if the port is an output, return the first input
    def trace(self):
        if not self.wires:
            return None

        if self in self.wires.inputs:
            if len(self.wires.outputs) < 1:
                # print('Warning:', str(self), 'is not connected to an output')
                return None
            assert len(self.wires.outputs) == 1
            return self.wires.outputs[0]

        if self in self.wires.outputs:
            if len(self.wires.inputs) < 1:
                # print('Warning:', str(self), 'is not connected to an input')
                return None
            assert len(self.wires.inputs) == 1
            return self.wires.inputs[0]

        return None

    # if the port is in the inputs, return the output
    def value(self):
        if not self.wires:
            return None

        if self in self.wires.inputs:
            if len(self.wires.outputs) < 1:
                # print('Warning:', str(self), 'is not connected to an output')
                return None
            #assert len(self.wires.outputs) == 1
            return self.wires.outputs[0]

        return None


    def driven(self):
        return self.value() is not None

    def wired(self):
        return self.trace() is not None

