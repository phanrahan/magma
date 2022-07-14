hw.module @test_when_nested_Array2TupleBitBits2Bit(%I_0_0_0: i1, %I_0_0_1: i2, %I_0_1_0: i1, %I_0_1_1: i2, %I_1_0_0: i1, %I_1_0_1: i2, %I_1_1_0: i1, %I_1_1_1: i2, %S: i1) -> (O_0_0: i1, O_0_1: i2, O_1_0: i1, O_1_1: i2) {
    %4 = sv.reg {name = "O0_reg"} : !hw.inout<!hw.array<2x!hw.struct<_0: i1, _1: i2>>>
    sv.alwayscomb {
        sv.bpassign %4, %I_0_0_1 : i2
        sv.if %S {
            sv.bpassign %4, %I_0_0_0 : i1
        }
    }
    %0 = sv.read_inout %4 : !hw.inout<!hw.array<2x!hw.struct<_0: i1, _1: i2>>>
    hw.output %0, %1, %2, %3 : i1, i2, i1, i2
}
