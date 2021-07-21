import os
import sys
from typing import Optional

import magma as m
from magma.testing import check_files_equal, SimpleMagmaProtocol


T = SimpleMagmaProtocol[m.Bits[8]]


def test_foo_type_magma_protocol():
    @m.sequential2()
    class Bar:
        def __init__(self):
            self.reg = m.Register(m.Bits[1])()

        def __call__(self, foo: T) -> T:
            self.reg = self.reg
            return foo.non_standard_operation()

    m.compile("build/test_foo_magma_protocol", Bar)
    assert check_files_equal(__file__, f"build/test_foo_magma_protocol.v",
                             f"gold/test_foo_magma_protocol.v")


def test_ite():

    @m.sequential2()
    class Bar:
        def __call__(self, cond: m.Bit, i0: T, i1: T) -> T:
            if cond:
                foo = i0
            else:
                foo = i1

            return foo.non_standard_operation()
