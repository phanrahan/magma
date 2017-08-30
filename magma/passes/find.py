from ..circuit import isdefinition

def find(cls, defn):
    if not isdefinition(cls):
        return defn

    for i in cls.instances:
        find( type(i), defn )

    name = cls.__name__
    if name not in defn:
        defn[name] = cls


