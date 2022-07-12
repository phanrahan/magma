import magma as m
import os
import sys


class BigTuple(m.Product):
    V1 = m.UInt[32]
    V2 = m.UInt[32]
    V3 = m.UInt[32]
    V4 = m.UInt[32]
    V5 = m.UInt[32]
    V6 = m.UInt[32]
    V7 = m.UInt[32]


@m.sequential2(debug=True)
class Top:
    def __init__(self):
        self.V1 = m.Register(m.UInt[32])()
        self.V2 = m.Register(m.UInt[32])()
        self.V3 = m.Register(m.UInt[32])()
        self.V4 = m.Register(m.UInt[32])()
        self.V5 = m.Register(m.UInt[32])()
        self.V6 = m.Register(m.UInt[32])()
        self.V7 = m.Register(m.UInt[32])()

    def __call__(self, I: BigTuple, SEL: m.Bit) -> BigTuple:
        t = m.product(
            V1=self.V1,
            V2=self.V2,
            V3=self.V3,
            V4=self.V4,
            V5=self.V5,
            V6=self.V6,
            V7=self.V7,
        )
        if SEL:
            new_t = I
        else:
            new_t = t

        self.V1 = new_t.V1
        self.V2 = new_t.V2
        self.V3 = new_t.V3
        self.V4 = new_t.V4
        self.V5 = new_t.V5
        self.V6 = new_t.V6
        self.V7 = new_t.V7
        return new_t


def test_tuple_perf():
    # for https://github.com/phanrahan/magma/issues/528#issuecomment-573510435
    m.compile("build/top", Top, output="coreir-verilog")
