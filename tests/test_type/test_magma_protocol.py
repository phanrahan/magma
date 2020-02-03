from typing import Optional
import magma as m
from magma.testing import check_files_equal

import sys
import os

TEST_SYNTAX_PATH = os.path.join(os.path.dirname(__file__), '../test_syntax')

sys.path.append(TEST_SYNTAX_PATH)

from test_sequential import DefineRegister, phi


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
        def __init__(self, val: Optional[m.Type] = None):
            if val is None:
                val = self.T()
            super().__init__(val)

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
