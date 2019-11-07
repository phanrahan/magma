import inspect
from collections.abc import Sequence
from hwtypes.adt import TupleMeta, ProductMeta, Product, Tuple
from functools import wraps

from .port import INPUT, OUTPUT, INOUT
from .compatibility import IntegerTypes
from .t import Type, deprecated, Flip, Undirected
from .array import Array
from .bits import Bits
from .tuple import tuple_
from .debug import debug_wire
from .port import report_wiring_error
from .ref import TupleRef, AnonRef


__all__ = ['wire']


@debug_wire
def wire(o, i, debug_info=None):
    # Wire(o, Circuit).
    if hasattr(i, 'interface'):
        i.wire(o, debug_info)
        return

    # Replace output Circuit with its output (should only be 1 output).
    if hasattr(o, 'interface'):
        # If wiring a Circuit to a Port then circuit should have 1 output.
        o_orig = o
        o = o.interface.outputs()
        if len(o) != 1:
            report_wiring_error(f"Can only wire circuits with one output. "
                                f"Argument 0 to wire `{o_orig.debug_name}` has "
                                f"outputs {o}", debug_info)
            return
        o = o[0]

    # If o is an input.
    if not isinstance(o, IntegerTypes) and o.is_input():
        # If i is not an input.
        if isinstance(i, IntegerTypes) or not i.is_input():
            # Flip i and o.
            i, o = o, i
    if isinstance(i._value, Array) and not isinstance(i._value, Bits):
        if isinstance(o, IntegerTypes):
            report_wiring_error(f'Cannot wire {o} (type={type(o)}) to {i.debug_name} (type={i.type_}) because conversions from IntegerTypes are only defined for Bits, not general Arrays', debug_info)  # noqa
            return
    if isinstance(o, IntegerTypes):
        o = Wire(name="", value=i.type_(o))

    # Wire(o, Type).
    i.wire(o, debug_info)


def wire_cast(fn):
    @wraps(fn)
    def wrapped(self, other):
        if not isinstance(other, Wire):
            other = Wire(value=self.type_(other))
        return fn(self, other)
    return wrapped


class Wire:
    def __init__(self, type_=None, name=None, value=None):
        if isinstance(name, str) or name is None:
            name = AnonRef(name)
        if isinstance(value, Wire):
            value = value._value
        self.name = name
        if value is not None:
            assert type_ is None
            self._value = value
            self.type_ = type(value)
        else:
            self.type_ = type_
            if isinstance(type_, ProductMeta):
                self._value = type_(**{k: Wire(v, TupleRef(self, k))._value for
                                       k, v in type_.field_dict.items()})
            elif isinstance(type_, TupleMeta):
                self._value = type_(*(Wire(v, TupleRef(self, i))._value for i,
                                      v in enumerate(type_.fields)))
            else:
                self._value = type_(name=name)
        assert self.type_ != Wire


    def _get_values(self):
        if isinstance(self._value, Product):
            return (getattr(self, key) for key in self._value.value_dict.keys())
        elif isinstance(self._value, Tuple):
            return (self[key] for key in self._value.value_dict.keys())
        elif isinstance(self._value, Array):
            return (self[i] for i in range(len(self._value)))
        else:
            return [self._value]

    def _get_items(self):
        if isinstance(self._value, Product):
            return ((key, getattr(self, key)) for key in self._value.value_dict.keys())
        elif isinstance(self._value, Tuple):
            return ((key, self[key]) for key in self._value.value_dict.keys())
        else:
            raise NotImplementedError()

    def const(self):
        if isinstance(self._value, Tuple):
            return all(x.const() for x in self._get_values())
        else:
            return self._value.const()

    def is_oriented(self, direction):
        if isinstance(self._value, Tuple):
            return all(x.is_oriented(direction) for x in self._get_values())
        else:
            return self._value.is_oriented(direction)

    @deprecated
    def isoriented(self, direction):
        return self.is_oriented(direction)

    def is_output(self):
        if isinstance(self._value, Tuple):
            return all(x.is_output() for x in self._get_values())
        else:
            return self._value.is_output()

    @deprecated
    def isoutput(self):
        return self.is_output()

    def is_input(self):
        if isinstance(self._value, Tuple):
            return all(x.is_input() for x in self._get_values())
        else:
            return self._value.is_input()

    @deprecated
    def isinput(self):
        return self.is_input()

    def is_inout(self):
        if isinstance(self._value, Tuple):
            return all(x.is_inout() for x in self._get_values())
        else:
            return self._value.is_inout()

    @deprecated
    def isinout(self):
        return self.is_inout()

    @debug_wire
    def wire(self, other, debug_info=None):
        if not isinstance(other, Wire):
            other = Wire(value=other)
        if isinstance(self._value, (Tuple, Array)):
            i, o = self._value, other._value
            if isinstance(self._value, Tuple):
                if not isinstance(other._value, (Flip(type(self._value)),
                                                 Undirected(type(self._value)))) and \
                        not isinstance(self._value, (Flip(type(other._value)),
                                                     Undirected(type(other._value)))):
                    report_wiring_error(f'Cannot wire {other.name} (type={type(o)}) to {self.name} (type={type(i)}) because {other.name} because {other.name} is not an instance of Flip(type({self.name}))', debug_info)  # noqa
                    return
            elif isinstance(self._value, Array):
                if not isinstance(o, Array):
                    if isinstance(o, IntegerTypes):
                        report_wiring_error(f'Cannot wire {o} (type={type(o)}) to {i.debug_name} (type={type(i)}) because conversions from IntegerTypes are only defined for Bits, not general Arrays', debug_info)  # noqa
                    else:
                        report_wiring_error(f'Cannot wire {o.debug_name} (type={type(o)}) to {i.debug_name} (type={type(i)}) because {o.debug_name} is not an Array', debug_info)  # noqa
                    return

                if i.N != o.N:
                    report_wiring_error(f'Cannot wire {o.debug_name} (type={type(o)}) to {i.debug_name} (type={type(i)}) because the arrays do not have the same length', debug_info)  # noqa
                    return

            for i_elem, o_elem in zip(self._get_values(), other._get_values()):
                if o_elem.is_input():
                    o_elem.wire(i_elem, debug_info)
                else:
                    i_elem.wire(o_elem, debug_info)
        else:
            self._value.wire(other._value, debug_info)

    def wired(self):
        if isinstance(self._value, Tuple):
            return all(x.wired() for x in self._value)
        return self._value.wired()

    def _driven(self, value):
        if isinstance(value, Tuple):
            return all(self._driven(x) for x in value)
        return value.driven()

    def driven(self):
        return self._driven(self._value)

    def trace(self):
        if isinstance(self._value, Tuple):
            trace = [x.trace() for x in self._value]
            if any(x is None for x in trace):
                return None
            if len(self) == len(trace) and self.iswhole(trace):
                return trace[0].name.tuple
            if isinstance(self._value, Product):
                return tuple_(dict(zip(self._value.fields, trace)))
            else:
                return tuple_(trace)
        return self._value.trace()

    def iswhole(self, values):

        if isinstance(self._value, Tuple):
            if any(x.anon() for x in values):
                return False

            # elements must be an tuple reference
            if any(not isinstance(x.name, TupleRef) for x in values):
                return False

            # elements must refer to the same tuple
            if not all(values[0].name.tuple is x.name.tuple for x in values):
                return False

            # elements should be numbered consecutively
            for i, field in enumerate(self._value.value_dict):
                if values[i].name.index != field:
                    return False
            return True
        else:
            return self._value.iswhole(values)

        return True


    def _val(self, val):
        if isinstance(val, Tuple):
            value = [self._val(x) for x in val]
            if any(x is None for x in value):
                return None
            if len(value) == len(self) and self.iswhole(value):
                return value[0].name.tuple
            if isinstance(value, Product):
                T = type("anon", (Tuple,), {k: type(v) for k, v in
                                            zip(val.field_dict.keys(),
                                                value)})
            else:
                T = Tuple[tuple(type(v) for v in value)]
            return T(*value)
        return val.value()

    def value(self):
        if isinstance(self._value, Tuple):
            return self._val(self._value)
        return self._value.value()

    def as_list(self):
        assert isinstance(self._value, Array)
        return [self._value[i] for i in range(len(self))]

    def __getattr__(self, name):
        if isinstance(self._value, Product) and \
                name in self._value.value_dict.keys():
            result = getattr(self._value, name)
            return Wire(name=TupleRef(self, name), value=result)
        return object.__getattribute__(self, name)

    def __getitem__(self, index):
        if isinstance(self._value, Tuple):
            result = self._value[index]
            if not isinstance(result, Wire):
                if isinstance(self._value, Product):
                    index = list(self._value.value_dict.keys())[index]
                return Wire(name=TupleRef(self, index), value=result)
            return result
        result = self._value[index]
        if not isinstance(result, Wire):
            return Wire(name=result.name, value=result)
        return result

    def __repr__(self):
        if not self.name.anon():
            return repr(self.name)
        elif isinstance(self._value, Array):
            ts = [repr(t) for t in self._get_values()]
            return 'array([{}])'.format(', '.join(ts))
        elif isinstance(self._value, Product):
            ts = [repr(t) for t in self._value.value_dict.values()]
            kts = ['{}={}'.format(k, v) for k, v in
                   zip(self._value.value_dict.keys(), ts)]
            return 'tuple_(dict({})'.format(', '.join(kts))
        elif isinstance(self._value, Tuple):
            ts = [repr(t) for t in self._value.value_dict.values()]
            return 'tuple_({})'.format(', '.join(ts))
        else:
            return repr(self._value)

    @property
    def debug_name(self):
        return self._value.debug_name

    def flatten(self):
        return sum([x.flatten() for x in self._get_values()], [])

    def __len__(self):
        if issubclass(self.type_, Tuple):
            return len(self.type_.field_dict)
        return len(self._value)

    def anon(self):
        return self.name.anon()

    @property
    def debug_info(self):
        return self._value.debug_info

    def __call__(self, other=None, **kwargs):
        if kwargs:
            assert issubclass(self.type_, Tuple)
            for k, v in kwargs.items():
                wire(v, getattr(self, k))
            return self
        else:
            wire(self, other)
            return self

    def ite(self, t_branch, f_branch):
        return self._value.ite(t_branch, f_branch)

    @wire_cast
    def __eq__(self, other):
        return self._value == other._value

    @wire_cast
    def __ne__(self, other):
        return self._value != other._value

    def __hash__(self):
        return hash(self._value)

    def __invert__(self):
        return ~self._value

    @wire_cast
    def __and__(self, other):
        return self._value & other._value

    @wire_cast
    def __or__(self, other):
        return self._value | other._value

    @wire_cast
    def __xor__(self, other):
        return self._value ^ other._value

    @wire_cast
    def __lshift__(self, other):
        return self._value << other._value

    @wire_cast
    def __rshift__(self, other):
        return self._value >> other._value

    def __neg__(self):
        return -self._value

    @wire_cast
    def __add__(self, other):
        return self._value + other._value

    @wire_cast
    def __sub__(self, other):
        return self._value - other._value

    @wire_cast
    def __mul__(self, other):
        return self._value * other._value

    @wire_cast
    def __floordiv__(self, other):
        return self._value // other._value

    @wire_cast
    def __truediv__(self, other):
        return self._value / other._value

    @wire_cast
    def __mod__(self, other):
        return self._value % other._value

    @wire_cast
    def __ge__(self, other):
        return self._value >= other._value

    @wire_cast
    def __gt__(self, other):
        return self._value > other._value

    @wire_cast
    def __le__(self, other):
        if not self.is_output():
            return self.wire(other)
        return self._value <= other._value

    @wire_cast
    def __lt__(self, other):
        return self._value < other._value

    def __int__(self):
        return int(self._value)

    @wire_cast
    def concat(self, other):
        return self._value.concat(other._value)

    def zext(self, other):
        return self._value.zext(other)

    def sext(self, other):
        return self._value.sext(other)

    def bvcomp(self, other):
        return self._value.bvcomp(other)

    def repeat(self, other):
        return self._value.repeat(other)

    def bits(self):
        return self._value.bits()

    def adc(self, other, carry):
        return self._value.adc(other, carry)
