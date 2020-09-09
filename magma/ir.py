from collections import OrderedDict
from .clock import wiredefaultclock

def compileclocks(cls):
    for instance in cls.instances:
        wiredefaultclock(cls, instance)

def compile(main):

    if main.name == "":
        code = "AnonymousCircuit("
        # Special case anonymous circuits for now
        for name, value in main.interface.ports.items():
            code += "\"{}\", {},".format(name, value)
        code = code[:-1] + ")"  # Replace final "," with a )
        return code

    compileclocks(main)

    defn = main.find(OrderedDict())

    code = ''
    for k, v in defn.items():
         #print('compiling', k)
         code += repr(v) + '\n'
    return code
