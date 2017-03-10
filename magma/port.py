import inspect
import traceback
import sys
__all__  = ['INPUT', 'OUTPUT', 'INOUT']
__all__ += ['flip']
__all__ += ['Port']

INPUT = 'input'
OUTPUT = 'output'
INOUT = 'inout'

def print_error(message, stack_frame):
    traceback.print_stack(f=stack_frame, limit=10)
    sys.stderr.write(message + "\n")

def get_original_wire_call_stack_frame():
    for frame in inspect.stack():
        if sys.version < (3, 5):
            function = inspect.getframeinfo(frame[0]).function
        else:
            function = frame.function
        if function not in ["wire", "connect", "get_original_wire_call_stack_frame"]:
            break
    if sys.version < (3, 5):
        return frame[0]
    else:
        return frame.frame

def flip(direction):
    assert direction in [INPUT, OUTPUT, INOUT]
    if   direction == INPUT:  return OUTPUT
    elif direction == OUTPUT: return INPUT
    elif direction == INOUT:  return INOUT

def mergewires(new, old):
    for i in old.inputs:
        if i not in new.inputs:
            new.inputs.append(i)
            i.wires = new

    for o in old.outputs:
        if o not in new.outputs:
            if len(new.outputs) > 0:
                print("Error: connecting more than one output to an input", o)
            new.outputs.append(o)
            o.wires = new

#
# A Wire has a list of input and output Ports.
#
class Wire:
    def __init__(self):
        self.inputs = []
        self.outputs = []

    def connect( self, o, i ):

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
                print_error("Error: using an input as an output {}".format(str(o)), 
                            get_original_wire_call_stack_frame())
                return

            if o not in self.outputs:
                if len(self.outputs) != 0:
                    print("Warning: adding an output to a wire with an output", str(o))
                #print('adding output', o)
                self.outputs.append(o)

        if not i.anon():
            #assert i.bit.direction is not None
            if i.bit.isoutput():
                print_error("Error: using an output as an input {}".format(str(i)),
                            get_original_wire_call_stack_frame())
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
                print("Error: output in the wire inputs:",)

        for o in self.outputs:
            if o.isinput():
                print("Error: input in the wire outputs:",)
                return False

        # check that this wire is only driven by a single output
        if len(self.outputs) > 1:
            print("Error: Multiple outputs on a wire:",)
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
    def wire(i, o):
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

        w.connect(o, i)

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

