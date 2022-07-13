hw.module @test_when_nested_Array2TupleBitBits2Bit(%I: !hw.array<2x!hw.array<2x!hw.struct<_0: i1, _1: i2>>>, %S: i1) -> (O: !hw.array<2x!hw.struct<_0: i1, _1: i2>>) {
    %1 = hw.constant 0 : i1
    %0 = hw.array_get %I[%1] : !hw.array<2x!hw.array<2x!hw.struct<_0: i1, _1: i2>>>
    %3 = hw.constant 1 : i1
    %2 = hw.array_get %I[%3] : !hw.array<2x!hw.array<2x!hw.struct<_0: i1, _1: i2>>>
    %5 = sv.reg {name = "O0_reg"} : !hw.inout<!hw.array<2x!hw.struct<_0: i1, _1: i2>>>
    sv.alwayscomb {
        sv.bpassign %5, %2 : !hw.array<2x!hw.struct<_0: i1, _1: i2>>
        sv.if %S {
            sv.bpassign %5, %0 : !hw.array<2x!hw.struct<_0: i1, _1: i2>>
        }
    }
    %4 = sv.read_inout %5 : !hw.inout<!hw.array<2x!hw.struct<_0: i1, _1: i2>>>
    hw.output %4 : !hw.array<2x!hw.struct<_0: i1, _1: i2>>
}
