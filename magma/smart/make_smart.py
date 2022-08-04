from magma.smart.smart_bits import SmartBits
from magma.type_utils import TypeTransformer, issint
from magma.value_utils import ValueTransformer, make_selector
from magma.t import Direction


class _SmartifyTypeTransformer(TypeTransformer):
    def visit_Bits(self, T):
        signed = issint(T)
        return SmartBits[len(T), signed]


class _InitializeSmartValueTransformer(ValueTransformer):
    def __init__(self, value):
        self._value = value

    def visit_Bits(self, value):
        sel = make_selector(value)
        init = sel.select(self._value)
        signed = issint(type(value))
        return SmartBits[len(value), signed](init)


def make_smart(value):
    Tsmart = _SmartifyTypeTransformer().visit(type(value))
    Tsmart = Tsmart.qualify(Direction.Undirected)
    smart_value = Tsmart()
    return _InitializeSmartValueTransformer(value).visit(smart_value)
