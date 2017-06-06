from __future__ import print_function
from .python_simulator import PythonSimulator
from .transforms import get_uniq_circuits
from .circuit import *
from .scope import *
from .array import ArrayType
from .bit import BitType
from .bits import seq2int
from .ref import InstRef
from code import compile_command
from builtins import input
import re
import readline
import cmd

__all__ = ['simulate']

class InstDecl:
    def __init__(self, varname, lineno, filename):
        self.varname = varname
        self.lineno = lineno
        self.filename = filename

    def __repr__(self):
        return self.filename + " line " + str(self.lineno) + ": " + self.varname

class DisplayExpr:
    idx = 0
    def __init__(self, string, vars, scope):
        self.object = eval(string, None, vars)
        self.scope = scope
        self.string = string

        DisplayExpr.idx += 1
        self.idx = DisplayExpr.idx

    def display(self, value):
        print("\t{}: {} = {}".format(self.idx, self.string, value))

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

class SimulationConsole(cmd.Cmd):
    intro = 'Magma Interactive Simulator.   Type help or ? to list commands.'

    def __init__(self, circuit, simulator):
        cmd.Cmd.__init__(self, completekey=None)

        self.scope = Scope()
        self.top_circuit = circuit
        self.simulator = simulator
        self.vars = {}
        self.update_vars()

        self.watchpoints = []
        self.display_exprs = []

        self.cycles = 0
        self.downedge = False

        self.aliases = { 'bt' : self.do_backtrace,
                         'x'  : self.do_examine } 

        self.update_prompt()


    def update_prompt(self):
        self.prompt = str(self.cycles) + ': ' + self.scope.value() + ' >>> '

    def default(self, line):
        if line == 'EOF':
            print()
            return True

        cmd, arg, line = self.parseline(line)
        if cmd in self.aliases:
            func = [self.aliases[cmd]]
        else:
            func = [getattr(self, n) for n in self.get_names() if n.startswith('do_' + cmd)]

        if len(func) == 1:
            return func[0](arg)
        elif len(func) > 1:
            print("Ambiguous command")
        else:
            self.console_evaluate(line)

    def precmd(self, line):
        self.advance_clock = False
        self.reeval = False
        self.skip_half = False
        self.skip_next = 0
        self.stepping = True

        return line
    
    def advance_simulator(self):
        self.simulator.step()
        self.simulator.evaluate()

        if not self.downedge:
            self.cycles += 1

        self.downedge = not self.downedge

        triggered_points = self.check_watchpoints()
        if triggered_points:
            print("Watchpoint hit:")
            for watchpoint in triggered_points:
                print("  " + get_bit_full_name(watchpoint.bit) + ": ", end='')
                self.log_val(watchpoint.bit, watchpoint.scope)
            return False

        return True

    def step_simulator(self):
        while self.skip_next > 0:
            if self.downedge and self.skip_half and not self.skip_next:
                self.skip_next = 1
            if self.skip_next and (not self.skip_half or not self.downedge):
                self.skip_next -= 1

            if not self.advance_simulator():
                break

    def continue_simulator(self):
        while self.advance_simulator():
            pass

    def postcmd(self, stop, line):
        if self.advance_clock:
            if self.stepping:
                self.step_simulator()
            else:
                self.continue_simulator()

        if self.reeval:
            self.simulator.evaluate()

        self.update_prompt()

        for e in self.display_exprs:
            e.display(self.format_val(e.object, e.scope))

        return stop
    
    def format_val(self, bit, scope, raw=False):
        val = self.simulator.get_value(bit, scope)
        if val is None:
            return "Doesn't exist"

        if raw:
            return val
        else:
            if not isinstance(bit, ArrayType):
                val = [val]
            return seq2int(val)

    def log_val(self, bit, scope, raw=False):
        print(self.format_val(bit, scope, raw))

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

    def console_evaluate(self, line):
        buf = line
        while True:
            try:
                code = compile_command(buf)
            except Exception as e: 
                print("Invalid python: {}".format(e))
                return

            if code is None:
                buf += '\n' + input("."*(len(self.prompt) - 1) + " ")
            else:
                break
        
        try:
            exec(code, None, self.vars)
        except Exception as e:
            print("Failed to execute: {}".format(e))

    def parse_next(self, num):
        self.advance_clock = True
        self.stepping = True

        if num:
            try:
                self.skip_next = int(num)
            except:
                print("Please provide an integer")
                self.skip_next = 0

        else:
            self.skip_next = 1

    def parse_print(self, arg, raw):
        if not arg:
            print('Please provide an argument')
            return

        try:
            printme = eval(arg, None, self.vars)
        except Exception as e:
            print("Failed to print: {}".format(e))
            return

        if isinstance(printme, BitType) or isinstance(printme, ArrayType):
            self.log_val(printme, self.scope, raw)
        elif isinstance(printme, CircuitType):
            inst_desc = describe_instance(printme) + ": "
            print(inst_desc)
            for name,bit in printme.interface.ports.items():
                print("  " + name + ": ", end='')
                self.log_val(bit, self.scope, raw)
        else:
            print("Can only print Bits and circuit instances")

    def do_quit(self, arg):
        return True

    def do_next(self, arg):
        self.skip_half = True
        self.parse_next(arg)

    def do_step(self, arg):
        self.skip_half = False
        self.parse_next(arg)

    def do_examine(self, arg):
        self.parse_print(arg, True)

    def do_print(self, arg):
        self.parse_print(arg, False)

    def do_watch(self, arg):
        if not arg:
            print('Provide a bit to watch')
            return

        try:
            watchme = eval(arg, None, self.vars)
        except Exception as e:
            print("Failed to watch: {}".format(e))
            return

        if not isinstance(watchme, BitType) and not isinstance(watchme, ArrayType):
            print("Can only watch bits or arrays")

        self.watchpoints.append(WatchPoint(watchme, self.scope, self.simulator))

    def do_delete(self, arg):
        if not arg:
            print('Provide a watchpoint to delete')
            return

        try:
            deleteme = eval(arg, None, self.vars)
        except Exception as e:
            print("Failed to delete watchpoint: {}".format(e))
            return

        for idx, watchpoint in enumerate(self.watchpoints):
            if watchpoint.bit == deleteme and watchpoint.scope == self.scope:
                del self.watchpoints[idx]
                return

        print('No watchpoint found to delete')

    def do_display(self, arg):
        if not arg:
            print('Provide an expression to display')
            return

        try:
            display_expr = DisplayExpr(arg, self.vars, self.scope)
        except Exception as e:
            print("Invalid argument to display: {}".format(e))
            return

        self.display_exprs.append(display_expr)

    def do_undisplay(self, arg):
        if not arg:
            print('Provide an index to stop displaying')
            return

        try:
            idx = int(arg)
        except:
            print("undisplay requires an integer")
            return

        self.display_exprs[:] = [e for e in self.display_exprs if e.idx != idx]

    def do_repeat(self, arg):
        self.reeval = True

    def do_up(self, arg):
        if self.scope.parent is not None:
            self.scope = self.scope.parent
            self.update_vars()
        else:
            print("Cannot go up")

    def do_descend(self, arg):
        try:
            inst = eval(arg, None, self.vars)
        except Exception as e:
            print("Invalid expression: {}".format(e))
            return

        if isinstance(inst, CircuitType):
            self.scope = Scope(parent=self.scope, instance=inst)
            self.update_vars()
        else:
            print("You must provide an instance to descend into")

    def do_info(self, arg):
        if arg == 'instances':
            print("")
            for inst in self.vars['circuit'].instances:
                desc_str = "  " + describe_instance(inst)
                print(desc_str)
            print("")
        elif arg == 'interface':
            print("\nCircuit Inputs:")
            for name, bit in self.vars['circuit'].interface.ports.items():
                if bit.isoutput():
                    if isinstance(bit, ArrayType):
                        print("  Bit[" + str(len(bit)) + "]:" + name)
                    else:
                        print("  Bit: " + name)

            print("\nCircuit Outputs:")
            for name, bit in self.vars['circuit'].interface.ports.items():
                if bit.isinput():
                    if isinstance(bit, ArrayType):
                        print("  Bit[" + str(len(bit)) + "]:" + name)
                    else:
                        print("  Bit: " + name)

            print("")

        else:
            print("I don't know how to give you info on that")

    def do_continue(self, arg): 
        self.advance_clock = True
        self.stepping = False

    def do_backtrace(self, arg):
        scopes = []
        curscope = self.scope
        while curscope is not None:
            locs.insert(0, curscope)
            curscope = curscope.parent

        print("Location stack: ")
        for s in scopes:
            print("  " + s.value())

    def do_change_input(self, arg):
        if arg is None:
            print('Provide a top level input to change')
            return

        args = arg.split()
        if len(args) != 2:
            print('Provide a circuit input and a new value')
            return

        bit = self.top_circuit.interface.ports.get(args[0])
        try:
            newval = eval(args[1], None, self.vars)
        except Exception as e:
            print("Invalid new value".format(e))
            return

        if bit is None or not bit.isoutput():
            print("b {}".format(bit))
            print('Not a top level circuit input')
            return

        self.simulator.set_value(bit, self.scope, newval)

    def run(self):
        self.simulator.evaluate()
        self.cmdloop()

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
