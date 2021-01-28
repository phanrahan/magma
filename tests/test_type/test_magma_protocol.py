from typing import Optional
import magma as m
from magma.testing import check_files_equal

import sys
import os


def test_foo_type_magma_protocol():
    class FooMeta(m.MagmaProtocolMeta):
        def _to_magma_(cls):
            # Need way to retrieve underlying magma type
            return cls.T

        def _qualify_magma_(cls, direction: m.Direction):
            # Need way to create a new version (e.g. give me a Foo with the
            # underlying type qualified to be an input)
            return cls[cls.T.qualify(direction)]

        def _flip_magma_(cls):
            # Need way to create a new version (e.g. give me a Foo with the
            # underlying type qualified to be an input)
            return cls[cls.T.flip()]

        def _from_magma_value_(cls, val: m.Type):
            # Need a way to create an instance of Foo from a value, this just
            # dispatches to the __init__ logic, but you could define any
            # custom behavior here
            return cls(val)

        def __getitem__(cls, T):
            return type(cls)(f"Foo{T}", (cls, ), {"T": T})

    class Foo(m.MagmaProtocol, metaclass=FooMeta):
        def __init__(self, val: Optional[m.Type] = None):
            if val is None:
                val = self.T()
            self._val = val

        def _get_magma_value_(self):
            # Need way to access underlying magma value
            return self._val

        def non_standard_operation(self):
            v0 = self._val << 2
            v1 = m.bits(self._val[0], len(self.T)) << 1
            return Foo(v0 | v1 | m.bits(self._val[0], len(self.T)))

    @m.sequential2
    class Bar:
        def __init__(self):
            self.reg: m.Bits[1] = m.Bits[1](0)

        def __call__(self, foo: Foo[m.Bits[8]]) -> m.Bits[8]:
            self.reg = self.reg
            return foo.non_standard_operation()

    m.compile("build/test_foo_magma_protocol", Bar)
    assert check_files_equal(__file__, f"build/test_foo_magma_protocol.v",
                             f"gold/test_foo_magma_protocol.v")
