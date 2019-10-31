import inspect
from collections.abc import Sequence
from hwtypes.adt import TupleMeta, ProductMeta, Product, Tuple

from .port import INPUT, OUTPUT, INOUT
from .compatibility import IntegerTypes
from .t import Type, deprecated, Flip
from .tuple import tuple_
from .debug import debug_wire
from .logging import info, warning, error
from .port import report_wiring_error
from .ref import TupleRef, AnonRef

__all__ = ['wire']


@debug_wire
def wire(o, i, debug_info=None):

    # Wire(o, Circuit)
    if hasattr(i, 'interface'):
        i.wire(o, debug_info)
        return

    # replace output Circuit with its output (should only be 1 output)
    if hasattr(o, 'interface'):
        # if wiring a Circuit to a Port
        # then circuit should have 1 output
        o_orig = o
        o = o.interface.outputs()
        if len(o) != 1:
            report_wiring_error(f'Can only wire circuits with one output. Argument 0 to wire `{o_orig.debug_name}` has outputs {o}', debug_info)  # noqa
            return
        o = o[0]

    # if o is an input
    if not isinstance(o, IntegerTypes) and o.is_input():
        # if i is not an input
        if isinstance(i, IntegerTypes) or not i.is_input():
            # flip i and o
            i, o = o, i

    #if hasattr(i, 'wire'):
    #    error('Wiring Error: The input must have a wire method -  {} to {}'.format(o, i))
    #    return

    # Wire(o, Type)
    i.wire(o, debug_info)


class Wire:
    def __init__(self, type_=None, name=None, value=None):
        if isinstance(name, str):
            name = AnonRef(name)
        self.name = name
        if value is not None:
            assert type_ is None
            self._value = value
            self.type_ = type(value)
        else:
            self.type_ = type_
            self._value = self.construct(type_, self.name)

    def construct(self, type_, name):
        if isinstance(type_, ProductMeta):
            return type_(**{k: self.construct(v, TupleRef(self, k)) for k, v in
                            type_.field_dict.items()})
        elif isinstance(type_, TupleMeta):
            return type_(self.construct(v, TupleRef(self, i)) for i, v in
                         enumerate(type_.fields))
        else:
            return type_(name=name)

    def _get_values(self):
        if isinstance(self._value, Product):
            return (getattr(self, key) for key in self._value.value_dict.keys())
        elif isinstance(self._value, Tuple):
            return (getattr(self, key) for key in self._value.fields())
        else:
            raise NotImplementedError()

    def _get_items(self):
        if isinstance(self._value, Product):
            return ((key, getattr(self, key)) for key in self._value.value_dict.keys())
        elif isinstance(self._value, Tuple):
            return ((key, getattr(self, key)) for key in self._value.fields())
        else:
            raise NotImplementedError()

    def is_output(self):
        if isinstance(self._value, Product):
            return all(x.is_output() for x in self._get_values())
        elif isinstance(self._value, Tuple):
            return all(x.is_output() for x in self._get_values())
        else:
            return self._value.is_output()

    @deprecated
    def isoutput(self):
        return self.is_output()

    def is_input(self):
        if isinstance(self._value, Product):
            return all(x.is_input() for x in self._get_values())
        elif isinstance(self._value, Tuple):
            return all(x.is_input() for x in self._get_values())
        else:
            return self._value.is_input()

    @deprecated
    def isinput(self):
        return self.is_input()

    def is_inout(self):
        if isinstance(self._value, Product):
            return all(x.is_inout() for x in self._get_values())
        elif isinstance(self._value, Tuple):
            return all(x.is_inout() for x in self._get_values())
        else:
            return self._value.is_inout()

    @deprecated
    def isinout(self):
        return self.is_inout()

    def wire(self, other, debug_info):
        assert isinstance(other, Wire)
        if isinstance(self._value, Tuple):
            i, o = self._value, other._value
            if not isinstance(other._value, Flip(type(self._value))):
                report_wiring_error(f'Cannot wire {other.name} (type={type(o)}) to {self.name} (type={type(i)}) because {other.name} because {other.name} is not an instance of Flip(type({self.name}))', debug_info)  # noqa
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

    def driven(self):
        if isinstance(self._value, Tuple):
            return all(x.driven() for x in self._value)
        return self._value.driven()

    def trace(self):
        if isinstance(self._value, Tuple):
            trace = [x.trace() for x in self._value]
            if any(x is None for x in trace):
                return None
            if self.iswhole(trace):
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
            if not all(values[0].name.tuple == x.name.tuple for x in values):
                return False

            # elements should be numbered consecutively
            for i, field in enumerate(self._value.value_dict):
                if values[i].name.index != field:
                    return False
            return True
        else:
            return self._value.iswhole(values)

        return True

    def value(self):
        if isinstance(self._value, Tuple):
            value = [x.value() for x in self._value]
            if any(x is None for x in value):
                return None
            if self.iswhole(value):
                return value[0].name.tuple
            if isinstance(self._value, Product):
                return tuple_(dict(zip(self._value.fields, value)))
            else:
                return tuple_(value)
        return self._value.trace()

    def __getattr__(self, name):
        if isinstance(self._value, Product) and \
                name in self._value.value_dict.keys():
            result = getattr(self._value, name)
            return Wire(name=TupleRef(self, name), value=result)
        return object.__getattribute__(self, name)

    def __getitem__(self, index):
        if isinstance(self._value, Tuple) and \
                index in self._value.value_dict.keys():
            result = getattr(self._value, index)
            return Wire(name=TupleRef(self, index), value=result)
        return self._value[index]

    def __repr__(self):
        if not isinstance(self.name, AnonRef) or self.name.name is not None:
            return repr(self.name)
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
        return self.name
