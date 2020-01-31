from typing import Optional
import magma as m
from magma.testing import check_files_equal


def test_foo_type_magma_protocol():
    class FooMeta(m.MagmaProtocolMeta):
        def _to_magma_(cls):
            # Need way to retrieve underlying magma type
            return cls.T

        def _from_magma_(cls, T):
            # Need way to create a new version (e.g. give me a Foo with the
            # underlying type qualified to be an input)
            return cls[T]

        def __getitem__(cls, T):
            return type(cls)(f"Foo{T}", (cls, ), {"T": T})

    class Foo(m.MagmaProtocol, metaclass=FooMeta):
        def __init__(self, val: Optional = None, name: Optional = None):
            if val is None:
                # Must define generic no val constructor with a specific name
                # for interface
                val = self.T(name=name)
            self._val = val

        def _get_magma_value_(self):
            return self._val

        def non_standard_operation(self):
            v0 = self._val << 2
            v1 = m.bits(self._val[0], len(self.T)) << 1
            return Foo(v0 | v1 | m.bits(self._val[0], len(self.T)))

    @m.circuit.sequential
    class Bar:
        def __init__(self):
            self.reg: m.Bits[1] = m.Bits[1](0)

        def __call__(self, foo: Foo[m.Bits[8]]) -> m.Bits[8]:
            self.reg = self.reg
            return foo.non_standard_operation()

    m.compile("build/test_foo_magma_protocol", Bar)
    assert check_files_equal(__file__, f"build/test_foo_magma_protocol.v",
                             f"gold/test_foo_magma_protocol.v")
