from collections.abc import Sequence, Mapping
from collections import OrderedDict
from hwtypes.adt import Tuple, Product, TupleMeta, ProductMeta
import magma as m
from .bitutils import int2seq
from .array import Array
from .bit import Digital, Bit
from .compatibility import IntegerTypes


#
# convert value to a tuple
#   *value = tuple from positional arguments
#   **kwargs = tuple from keyword arguments
#
def tuple_(value, n=None, t=Tuple):
    if isinstance(value, t):
        return value

    if not isinstance(value, (Digital, Array, IntegerTypes, Sequence, Mapping)):
        raise ValueError(
            "bit can only be used on a Bit, an Array, or an int; not {}".format(type(value)))

    decl = OrderedDict()
    args = []

    if isinstance(value, IntegerTypes):
        if n is None:
            n = max(value.bit_length(),1)
        value = int2seq(value, n)
    elif isinstance(value, Digital):
        value = [value]
    elif isinstance(value, Array):
        value = [value[i] for i in range(len(value))]

    if isinstance(value, Sequence):
        ts = list(value)
        for i in range(len(ts)):
            if isinstance(ts[i], m.Wire):
                args.append(ts[i]._value)
                decl[i] = ts[i].type_
            else:
                args.append(ts[i])
                decl[i] = type(ts[i])
    elif isinstance(value, Mapping):
        for k, v in value.items():
            if isinstance(v, m.Wire):
                decl[k] = v.type_
                args.append(v._value)
            else:
                args.append(v)
                decl[k] = type(v)

    T = type("anon", (t,), decl)
    return m.Wire(name="", value=T(*args))


def namedtuple(**kwargs):
    return tuple_(kwargs, t=Product)
