from hwtypes.adt import Tuple, Product, TupleMeta, ProductMeta


from .bitutils import int2seq
from .array import Array
from .bit import Digital, Bit, VCC, GND

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
            args.append(ts[i])
            decl[i] = type(ts[i])
    elif isinstance(value, Mapping):
        for k, v in value.items():
            args.append(v)
            decl[k] = type(v)

    return type("anon", (t,), decl)(*args)


def namedtuple(**kwargs):
    return tuple_(kwargs, t=Product)
