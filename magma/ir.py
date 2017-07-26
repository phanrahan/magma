from collections import OrderedDict
from .wire import wiredefaultclock

def compileclocks(cls):
    for instance in cls.instances:
        wiredefaultclock(cls, instance)

def compile(main):

    compileclocks(main)

    defn = main.find(OrderedDict())

    code = ''
    for k, v in defn.items():
         #print('compiling', k)
         code += repr(v) + '\n'
    return code
