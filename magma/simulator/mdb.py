from __future__ import print_function
from .python_simulator import PythonSimulator
from ..passes.debug_name import DebugNamePass
from ..is_definition import isdefinition
from ..circuit import CircuitType, EndCircuit
from ..scope import *
from ..array import Array
from ..bit import Bit
from ..bitutils import seq2int, int2seq
from ..ref import InstRef, DefnRef
from ..compatibility import builtins
from magma.waveform import waveform
from code import compile_command
import re
import sys
if sys.platform == "linux" or sys.platform == "linux2" or sys.platform == "darwin":
    import readline
import cmd

__all__ = ['simulate', 'SimulationConsole']

class DisplayExpr:
    idx = 0
    def __init__(self, bit, string, scope):
        self.object = bit
        self.scope = scope
        self.string = string

        DisplayExpr.idx += 1
        self.idx = DisplayExpr.idx

    def display(self, value):
        print("\t{}: {} = {}".format(self.idx, self.string, value))

def print_err(str):
    print(str, file=sys.stderr)

def split_index(str):
    r = re.compile(r"^([a-zA-Z]+)((?:\[[0-9]+\])+)$")
    match = r.match(str)
    if match is None:
        return None

    idxr = re.compile(r"\[([0-9]+)\]")
    idx_match = idxr.findall(match[2])

    return match[1], [int(i) for i in idx_match]

def convert_to_bools(val, bit):
    if isinstance(val, int):
        return int2seq(val, len(bit))
    elif isinstance(val, bool):
        return val
    elif isinstance(val, list):
        newval = []
        for i,v in enumerate(val):
            newval.append(convert_to_bools(v, bit[i]))
        return newval

def describe_instance(inst):
    desc_str = type(inst).__name__ + ": "
    if inst.decl is not None:
        desc_str += inst.decl.varname + " @ " + inst.decl.filename + ":" + str(inst.decl.lineno)

    desc_str += " (" + inst.name + ")"
    return desc_str

def describe_interface(interface):
    print("\nInterface Inputs:")
    for name, bit in interface.ports.items():
        if bit.is_output():
            if isinstance(bit, Array):
                print("  Bit[" + str(len(bit)) + "]:" + name)
            else:
                print("  Bit: " + name)

    print("\nInterface Outputs:")
    for name, bit in interface.ports.items():
        if bit.is_input():
            if isinstance(bit, Array):
                print("  Bit[" + str(len(bit)) + "]:" + name)
            else:
                print("  Bit: " + name)

    print("")

def get_bit_full_name(bit):
    name = bit.name
    if isinstance(name, InstRef):
        return name.inst.name + "." + name.name
    elif isinstance(name, DefnRef):
        return str(name.defn) + '.' + name.name
    elif isinstance(name, ArrayRef):
        arrayname = get_bit_full_name(name.array)
        return arrayname + "[" + str(name.index) + "]"
    else:
        return ""

def format_val(val, bit, raw):
    # Is an array of arrays?
    if isinstance(val, list) and len(val) > 0 and isinstance(val[0], list):
        s = '['
        for i, v in enumerate(val):
            s += str(format_val(v, bit[i], raw))
            if i < len(val) - 1:
                s += ", "
        s += ']'
        return s
    else:
        if raw:
            return "".join(['1' if e else '0' for e in reversed(val)])
        else:
            if not isinstance(bit, Array) or isinstance(val, bool):
                val = [val]
            return seq2int(val)

class SimulationConsoleException(Exception):
    pass

class SimulationConsole(cmd.Cmd):
    def __init__(self, circuit, simulator):
        cmd.Cmd.__init__(self, completekey=None)

        self.scope = Scope()
        self.top_circuit = circuit
        self.simulator = simulator
        self.vars = {}
        self.update_vars()

        self.display_exprs = []

        self.cycles = 0
        self.clock_high = False

        self.aliases = { 'x'  : self.do_examine,
                         'd'  : self.do_descend,
                         'rn' : self.do_reverse_cycle,
                         'rs' : self.do_reverse_step }

        self.update_prompt()

    def print_watchpoints(self, points):
        print("Watchpoint hit:")
        for watchpoint in points:
            print("  " + get_bit_full_name(watchpoint.bit) + ": ", end='')
            self.log_val(watchpoint.bit, watchpoint.scope)

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
            print_err("Ambiguous command")
        else:
            self.console_evaluate(line)

    def precmd(self, line):
        self.advance_clock = False
        self.reeval = False
        self.skip_half = False
        self.skip_next = 0
        self.stepping = True
        self.reversing = False

        return line

    def reverse_simulator(self):
        if self.clock_high and self.cycles == 0: return

        reversecount = self.skip_next
        if self.skip_half:
            reversecount *= 2
            if not self.clock_high:
                reversecount -= 1

        for i in range(reversecount):
            state = self.simulator.rewind(1)
            self.clock_high = state.clock
            if self.clock_high:
                self.cycles -= 1

            if state.triggered_points:
                self.print_watchpoints(state.triggered_points)
                return False

    def step_simulator(self):
        n = self.skip_next 
        if self.skip_half:
            n *= 2
            if self.clock_high:
                n -= 1

        state = self.simulator.advance(n)
        self.clock_high = state.clock
        self.cycles += state.cycles
        if state.triggered_points:
            self.print_watchpoints(state.triggered_points)

    def continue_simulator(self):
        state = self.simulator.cont()
        self.print_watchpoints(state.triggered_points)
        self.clock_high = state.clock
        self.cycles += state.cycles

    def postcmd(self, stop, line):
        if self.reversing:
            self.reverse_simulator()

        elif self.advance_clock:
            if self.stepping:
                self.step_simulator()
            else:
                self.continue_simulator()

        if self.reeval:
            self.simulator.evaluate(True)

        self.update_prompt()

        for e in self.display_exprs:
            e.display(self.get_formatted_val(e.object, e.scope))

        return stop
    
    def get_formatted_val(self, bit, scope, raw=False):
        val = self.simulator.get_value(bit, scope)
        if val is None:
            return "Doesn't exist"

        return format_val(val, bit, raw)

    def log_val(self, bit, scope, raw=False):
        print(self.get_formatted_val(bit, scope, raw))

    def update_vars(self):
        self.vars.clear()
        self.vars['top'] = self.top_circuit

        if self.scope.inst is None:
            self.vars['self'] = self.top_circuit
        else:
            self.vars['self'] = type(self.scope.inst)

        instances = self.vars['self'].instances
        for inst in instances:
            self.vars[inst.name] = inst
            if inst.decl is not None:
                self.vars[inst.decl.varname] = inst

    def console_evaluate(self, line):
        buf = line
        while True:
            try:
                code = compile_command(buf)
            except Exception as e: 
                print_err("Invalid python: {}".format(e))
                return

            if code is None:
                buf += '\n' + builtins.input("."*(len(self.prompt) - 1) + " ")
            else:
                break
        
        try:
            exec(code, None, self.vars)
        except Exception as e:
            print_err("Failed to execute: {}".format(e))


    def parse_circuit(self, name):
        components = name.split('.')
        if len(components) < 1:
            raise SimulationConsoleException("Need at least instance name")
        
        topname = components.pop(0)
        cur = eval(topname, None, self.vars)

        scope = Scope() if cur == self.top_circuit else self.scope

        for idx, comp_name in enumerate(components):
            defn = type(cur) if isinstance(cur, CircuitType) else cur
            index_match = split_index(comp_name)
            bit_idx = None
            if index_match is not None:
                comp_name = index_match[0]
                bit_idx = index_match[1]

            # Last iteration, check for bit first
            if idx == len(components) - 1 and comp_name in cur.interface.ports:
                if bit_idx is None:
                    return cur.interface.ports[comp_name], scope
                else:
                    port = cur.interface.ports[comp_name]
                    for i in bit_idx:
                        port = port[i]
                    return port, scope

            found = False
            for inst in defn.instances:
                if inst.name == comp_name or (inst.decl is not None and inst.decl.varname == comp_name):
                    # Descend into previous instance's scope
                    if cur != self.top_circuit:
                        scope = Scope(parent=scope, instance=cur)

                    cur = inst
                    found = True
                    break

            if not found:
                raise SimulationConsoleException("Invalid name component '{}'".format(comp_name))

        return cur, scope

    def safe_parse_inst(self, name):
            inst, scope = self.parse_circuit(name)
            if not isinstance(inst, CircuitType):
                raise SimulationConsoleException("not an instance")

            return inst

    def parse_next(self, num):
        self.advance_clock = True
        self.stepping = True

        if num:
            try:
                self.skip_next = int(num)
            except:
                print_err("Please provide an integer")
                self.skip_next = 0

        else:
            self.skip_next = 1

    def parse_print(self, arg, raw):
        if not arg:
            print_err('Please provide an argument')
            return

        try:
            printme, scope = self.parse_circuit(arg)
        except Exception as e:
            print_err("Failed to print: {}".format(e))
            return

        if isinstance(printme, Bit) or isinstance(printme, Array):
            self.log_val(printme, scope, raw)
        elif isinstance(printme, CircuitType):
            inst_desc = describe_instance(printme) + ": "
            print(inst_desc)
            for name, bit in printme.interface.ports.items():
                print("  " + name + ": ", end='')
                self.log_val(bit, scope, raw)
        else:
            print_err("Can only print Bits and circuit instances")

    def do_quit(self, arg):
        'quit: Exit the simulator'
        return True

    def do_next(self, arg):
        'next [N]: Advance the clock for N cycles. N defaults to 1 if not provided.'
        self.skip_half = True
        self.parse_next(arg)

    def do_step(self, arg):
        'step [N]: Toggle the clock N times. N defaults to 1 if not provided.'
        self.skip_half = False
        self.parse_next(arg)

    def do_reverse_step(self, arg):
        'reverse_step N: rewinds the circuit N half cycles'
        self.reversing = True
        self.skip_half = False
        self.parse_next(arg)

    def do_reverse_cycle(self, arg):
        'reverse_cycle N: rewinds the circuit N cycles'
        self.reversing = True
        self.skip_half = True
        self.parse_next(arg)

    def do_examine(self, arg):
        'examine BIT: prints the current value of BIT as an array of booleans. Shortcut: x BIT.'
        self.parse_print(arg, True)

    def do_print(self, arg):
        'print BIT: prints the current value of BIT interpreted as an unsigned integer.'
        self.parse_print(arg, False)

    def do_watch(self, arg):
        'watch BIT [VALUE]: sets a watchpoint on BIT.\nThe simulator will interrupt and return to the console when BIT changes value.\nIf the optional argument VALUE is passed in, the simulator will interrupt only when BIT is equal to VALUE.'
        if not arg:
            print_err('Provide a bit to watch')
            return

        args = arg.split()
        bitname = args[0]

        try:
            watchme, scope = self.parse_circuit(bitname)
        except Exception as e:
            print_err("Failed to watch: {}".format(e))
            return

        if len(args) == 2:
            try:
                value = eval(args[1], None, self.vars)
                if isinstance(value, int):
                    value = [bool(i) for i in int2seq(value, len(watchme))]

                if not isinstance(value, list) or not isinstance(value[0], bool):
                    raise SimulationConsoleException("Invalid watch value")
            except Exception as e:
                print_err("Cannot watch for value {}: {}".format(args[1], e))
                return
        else:
            value = None

        if not isinstance(watchme, Bit) and not isinstance(watchme, Array):
            print_err("Can only watch bits or arrays")

        watch_num = self.simulator.add_watchpoint(watchme, scope, value)
        print('Watchpoint {} on {}'.format(watch_num, arg))

    def do_delete(self, arg):
        'delete N: deletes watchpoint N.'
        if not arg:
            print_err('Please provide a watchpoint number')
            return

        try:
            watch_num = int(arg)
        except:
            print_err("delete requires an integer")
            return

        found = self.simulator.delete_watchpoint(watch_num)
        if not found:
            print_err('No watchpoint number {}'.format(watch_num))

    def do_display(self, arg):
        'display BIT: repeatedly prints the value of BIT each time the simulator stops.'

        if not arg:
            print_err('Provide an expression to display')
            return

        try:
            bit, scope = self.parse_circuit(arg)
            if not isinstance(bit, Bit) and not isinstance(bit, Array):
                raise SimulationConsoleException("Can only display bits or arrays")

            display_expr = DisplayExpr(bit, arg, scope)
        except Exception as e:
            print_err("Invalid argument to display: {}".format(e))
            return

        self.display_exprs.append(display_expr)

    def do_undisplay(self, arg):
        'undisplay N: stops displaying the bit at index N.'
        if not arg:
            print_err('Provide an index to stop displaying')
            return

        try:
            idx = int(arg)
        except:
            print_err("undisplay requires an integer")
            return

        for i,e in enumerate(self.display_exprs):
            if e.idx == idx:
                del self.display_exprs[i]
                return 
        print_err('No display number {}'.format(idx))

    def do_up(self, arg):
        "up: Change to the parent circuit's scope."
        if self.scope.parent is not None:
            self.scope = self.scope.parent
            self.update_vars()
        else:
            print_err("Cannot go up")

    def do_descend(self, arg):
        "descend INSTANCE: update the current scope to be inside INSTANCE."
        try:
            inst, scope = self.parse_circuit(arg)

            if not isdefinition(type(inst)):
                print_err("Cannot descend into primitives")
                return
        except Exception as e:
            print_err("Cannot switch scope to '{}': {}".format(arg, e))
            return

        if isinstance(inst, CircuitType):
            self.scope = Scope(parent=scope, instance=inst)
            self.update_vars()
        elif inst == self.top_circuit:
            self.scope = Scope()
            self.update_vars()
        else:
            print_err("You must provide an instance to descend into")

    def do_info(self, arg):
        """info instances|interface|watchpoints:
     instances [INSTANCE]: Display all the instances in the current scope or in INSTANCE if provided
     interface [INSTANCE]: Display the interface bits of the current scope's circuit or in INSTANE if provided
     watchpoints: Display currently active watchpoints"""
        args = arg.split()
        action = args[0]
        instname = args[1] if len(args) == 2 else None
        if action == 'instances':
            defn = self.vars['self']
            if instname:
                try:
                    inst = self.safe_parse_inst(instname)
                except Exception as e:
                    print_err("Cannot get info on '{}': {}".format(instname, e))
                    return
                defn = type(inst)

                if not isdefinition(defn):
                    print_err("Cannot get instances in '{}' because it is a primitive".format(instname))
                    return

            print("")
            for inst in defn.instances:
                desc_str = "  " + describe_instance(inst)
                print(desc_str)
            print("")

        elif action == 'interface':
            defn = self.vars['self']
            if instname:
                try:
                    inst = self.safe_parse_inst(instname)
                except Exception as e:
                    print_err("Cannot get info on '{}': {}".format(instname, e))
                    return
                defn = type(inst)

            describe_interface(defn.interface)
        elif arg == 'watchpoints':
            print("TODO")
        else:
            print_err("I don't know how to give you info on that")

    def do_continue(self, arg): 
        "continue: continue cycling the simulator's clock and evaluating until a watchpoint is hit."
        self.advance_clock = True
        self.stepping = False

    def do_location(self, arg):
        "location: Print the trace of parent scopes of the current scope."
        scopes = []
        curscope = self.scope
        while curscope is not None:
            scopes.insert(0, curscope)
            curscope = curscope.parent

        print("Scope stack: ")
        for s in scopes:
            print("  " + s.value())

    def do_assign(self, arg):
        "assign BIT NEWVAL: sets BIT to NEWVAL. BIT must be an input to the top level circuit."
        if arg is None:
            print_err('Provide a top level input to change')
            return

        args = arg.split(' ', 1)

        try:
            bit = eval(args[0], None, self.vars)
        except Exception as e:
            print_err("Invalid bit for assignment: {}".format(e))
            return

        if bit not in self.top_circuit.interface.outputs():
            print_err("Can only assign values to inputs in the top level circuit")
            return

        try:
            newval = eval(args[1], None, self.vars)
        except Exception as e:
            print_err("Invalid new value".format(e))
            return

        newval = convert_to_bools(newval, bit)

        self.simulator.set_value(bit, newval, self.scope)
        self.reeval = True

    def do_waveform(self, arg):
        if not arg:
            print_err('Please a provide wire')
            return

        try:
            waveme, scope = self.parse_circuit(arg)
        except Exception as e:
            print_err("Invalid argument for waveform: {}".format(e))
            return

        if not isinstance(waveme, Bit) and not isinstance(waveme, Array):
            print_err("Can only provide waveforms for wires")
            return

        labels = [arg]
        signals = []

        for i in range(self.cycles - 1):
            val = self.simulator.get_value(waveme, scope)
            signals.insert(0, [seq2int(val)])
            self.simulator.rewind(2)

        for i in range(self.cycles - 1):
            self.simulator.step()
            self.simulator.step()

        waveform(signals, labels)

    def run(self):
        self.simulator.evaluate()

        print('Magma Interactive Simulator.   Type help or ? to list commands.')
        while True:
            try:
                self.cmdloop()
                break;
            except KeyboardInterrupt:
                print_err('\nKeyboardInterrupt')

    # For test infra
    def runcmd(self, line):
        line = self.precmd(line)
        stop = self.onecmd(line)
        self.postcmd(stop, line)

def simulate(main, simulator_type=PythonSimulator):
    EndCircuit()
    simulator = simulator_type(main, main.CLK)

    DebugNamePass(main).run()

    console = SimulationConsole(main, simulator)
    console.run()
