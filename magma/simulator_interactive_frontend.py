from __future__ import print_function
from .python_simulator import PythonSimulator
from .transforms import get_uniq_circuits
from .circuit import *
from .scope import *
from .array import ArrayType
from .bit import BitType
from .bits import seq2int
from .ref import InstRef
from code import InteractiveConsole
import re

__all__ = ['simulate']

class InstDecl:
    def __init__(self, varname, lineno, filename):
        self.varname = varname
        self.lineno = lineno
        self.filename = filename

    def __repr__(self):
        return self.filename + " line " + str(self.lineno) + ": " + self.varname

class WatchPoint:
    def __init__(self, bit, scope, simulator):
        self.bit = bit 
        self.scope = scope
        self.simulator = simulator
        self.old_val = self.simulator.get_value(self.bit, self.scope)

    def was_triggered(self):
        new_val = self.simulator.get_value(self.bit, self.scope)
        triggered = new_val != self.old_val
        self.old_val = new_val

        return triggered

def describe_instance(inst):
    desc_str = type(inst).__name__ + ": "
    if inst.decl is not None:
        desc_str += inst.decl.varname + " @ " + inst.decl.filename + ":" + str(inst.decl.lineno)

    desc_str += " (" + inst.name + ")"
    return desc_str

def get_bit_full_name(bit):
    name = bit.name
    if isinstance(name, InstRef):
        return name.inst.name + "." + name.name
    elif isinstance(name, DefnRef):
        return name.defn + '.' + name.name
    elif isinstance(name, ArrayRef):
        arrayname = get_bit_full_name(name.array)
        return arrayname + "[" + str(name.index) + "]"
    else:
        return ""

class SimulationConsole:
    def __init__(self, circuit, simulator):
        self.scope = Scope()
        self.top_circuit = circuit
        self.simulator = simulator
        self.vars = {}
        self.update_vars()

        self.console = InteractiveConsole(locals=self.vars)
        self.watchpoints = []

    def log_val(self, bit, scope, raw=False):
        val = self.simulator.get_value(bit, scope)
        if val is None:
            print("Doesn't exist")
            return

        if raw:
            print(val)
        else:
            if not isinstance(bit, ArrayType):
                val = [val]
            print(seq2int(val))

    def update_vars(self):
        self.vars.clear()

        if self.scope.inst is None:
            self.vars['circuit'] = self.top_circuit
        else:
            self.vars['circuit'] = type(self.scope.inst)

        instances = self.vars['circuit'].instances
        for inst in instances:
            self.vars[inst.name] = inst
            if inst.decl is not None:
                self.vars[inst.decl.varname] = inst

    def check_watchpoints(self):
        triggered_points = []
        for watchpoint in self.watchpoints:
            if watchpoint.was_triggered():
                triggered_points.append(watchpoint)

        return triggered_points

    def console_evaluate(self, user_input):
        try:
            return self.console.push(user_input)
        except (SyntaxError, OverflowError, ValueError):
            self.console.showsyntaxerror()
            return False

    def prompt(self, triggered_points, cycles):
        toggle_clock = True
        skip_half = False
        skip_next = 0
        stepping = True

        if triggered_points:
            print("Watchpoint hit:")
            for watchpoint in triggered_points:
                print("  " + get_bit_full_name(watchpoint.bit) + ": ", end='')
                self.log_val(watchpoint.bit, watchpoint.scope)

        while True:
            prompt = str(cycles) + ": " + self.scope.value() + " >>> "

            user_in = self.console.raw_input(prompt=prompt)
            in_stripped = user_in.strip()
            was_command = False

            next_regex = r"^(n|s)( [0-9]+)?$"
            next_match = re.match(next_regex, in_stripped)
            if next_match:
                try:
                    was_command = True
                    if next_match.group(1) == 'n':
                        skip_half = True

                    skip_next = 1
                    if len(next_match.groups()) == 2 and next_match.group(2) is not None:
                        skip_next = int(next_match.group(2))

                    break
                except ValueError:
                    print("Please provide an integer")

            print_regex = r"^(p|x) (.+)"
            print_match = re.match(print_regex, in_stripped)
            if print_match:
                was_command = True
                try:
                    raw = print_match.group(1) == 'x'
                    printme = eval(print_match.group(2), None, self.vars)
                    if isinstance(printme, BitType) or isinstance(printme, ArrayType):
                        self.log_val(printme, self.scope, raw)
                    elif isinstance(printme, CircuitType):
                        inst_desc = describe_instance(printme) + ": "
                        print(inst_desc)
                        for name,bit in printme.interface.ports.items():
                            print("  " + name + ": ", end='')
                            self.log_val(bit, self.scope)
                    else:
                        print("Can only print Bits and circuit instances")
                except ValueError:
                    print("Couldn't print")

            watch_regex = r"^(w|watch) (.+)$"
            watch_match = re.match(watch_regex, in_stripped)
            if watch_match:
                was_command = True
                try:
                    watchme = eval(watch_match.group(2), None, self.vars)
                    if not isinstance(watchme, BitType) and not isinstance(watchme, ArrayType):
                        print("Can only watch bits or arrays")

                    self.watchpoints.append(WatchPoint(watchme, self.scope, self.simulator))

                except Exception as e:
                    print("Failed to watch {}".format(e))

            if in_stripped == 'r' or in_stripped == 'rerun':
                was_command  = True
                toggle_clock = False
                break

            if in_stripped == 'u' or in_stripped == 'up':
                was_command = True
                if self.scope.parent is not None:
                    self.scope = self.scope.parent
                    self.update_vars()
                else:
                    print("Cannot go up")

            down_regex = r"^(d|down) (.+)$"
            down_match = re.match(down_regex, in_stripped)
            if down_match:
                was_command = True
                try:
                    inst = eval(down_match.group(2), None, self.vars)
                    if inst:
                        self.scope = Scope(parent=self.scope, instance=inst)
                        self.update_vars()
                    else:
                        print("You must provide an instance")

                except:
                    print("Invalid expression")

            info_regex = r"^info (.+)$"
            info_match = re.match(info_regex, in_stripped)
            if info_match:
                was_command = True
                if info_match.group(1) == 'instances':
                    print("")
                    for inst in self.vars['circuit'].instances:
                        desc_str = "  " + describe_instance(inst)
                        print(desc_str)
                    print("")
                elif info_match.group(1) == 'interface':
                    print("\nCircuit Inputs:")
                    for name,bit in self.vars['circuit'].interface.ports.items():
                        if bit.isoutput():
                            if isinstance(bit, ArrayType):
                                print("  Bit[" + str(len(bit)) + "]:" + name)
                            else:
                                print("  Bit: " + name)

                    print("\nCircuit Outputs:")
                    for name,bit in self.vars['circuit'].interface.ports.items():
                        if bit.isinput():
                            if isinstance(bit, ArrayType):
                                print("  Bit[" + str(len(bit)) + "]:" + name)
                            else:
                                print("  Bit: " + name)

                    print("")

                else:
                    print("I don't know how to give you info on that")

            if in_stripped == 'c' or in_stripped == 'continue':
                was_command = True
                stepping = False
                skip_next = 1
                break

            if in_stripped == 'bt' or in_stripped == 'backtrace':
                was_command = True
                scopes = []
                curscope = self.scope
                while curscope is not None:
                    locs.insert(0, curscope)
                    curscope = curscope.parent

                print("Location stack: ")
                for s in scopes:
                    print("  " + s.value())

            if not was_command:
                while True:
                    if self.console_evaluate(user_in):
                        user_in = self.console.raw_input(prompt="."*(len(prompt) - 1) + " ")
                    else:
                        break

        return (toggle_clock, skip_half, skip_next, stepping)

    def run(self):
        cycles = 0
        skip_next = 0
        skip_half = True
        stepping = True
        downedge = False

        while True:
            self.simulator.evaluate()
            triggered_points = self.check_watchpoints()

            toggleclock = True

            if triggered_points or skip_next == 0:
                (toggleclock, skip_half, skip_next, stepping) = self.prompt(triggered_points, cycles)

            if toggleclock:
                if stepping:
                    if downedge and skip_half and not skip_next:
                        skip_next = 1
                    if skip_next and (not skip_half or not downedge):
                        skip_next -= 1

                if not downedge:
                    cycles += 1

                self.simulator.step()
                downedge = not downedge

def add_debug_info(main):
    circuits = get_uniq_circuits(main)
    for circuit in circuits:
      for inst in circuit.instances:
          stack = inst.stack
          inst.decl = None

          for frame_info in stack:
              local_vars = frame_info.frame.f_locals.items()
              for name, var in local_vars:
                  if var is inst:
                      inst.decl = InstDecl(name, frame_info.lineno, frame_info.frame.f_code.co_filename)
                      break

def simulate(main):
    EndCircuit()
    simulator = PythonSimulator(main)
    
    add_debug_info(main)

    console = SimulationConsole(main, simulator)
    console.run()
