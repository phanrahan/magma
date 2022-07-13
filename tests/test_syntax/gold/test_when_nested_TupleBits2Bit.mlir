hw.module @test_when_nested_TupleBits2Bit(%I: !hw.array<2x!hw.struct<_0: i2, _1: i1>>, %S: i1) -> (O: !hw.struct<_0: i2, _1: i1>) {
    %1 = hw.constant 0 : i1
    %0 = hw.array_get %I[%1] : !hw.array<2x!hw.struct<_0: i2, _1: i1>>
    %2 = hw.struct_extract %0["_0"] : !hw.struct<_0: i2, _1: i1>
    %3 = hw.struct_extract %0["_1"] : !hw.struct<_0: i2, _1: i1>
    %5 = hw.constant 1 : i1
    %4 = hw.array_get %I[%5] : !hw.array<2x!hw.struct<_0: i2, _1: i1>>
    %6 = hw.struct_extract %4["_0"] : !hw.struct<_0: i2, _1: i1>
    %7 = hw.struct_extract %4["_1"] : !hw.struct<_0: i2, _1: i1>
    %10 = sv.reg {name = "O0_reg"} : !hw.inout<i2>
    %11 = sv.reg {name = "O1_reg"} : !hw.inout<i1>
    sv.alwayscomb {
        sv.bpassign %10, %6 : i2
        sv.bpassign %11, %7 : i1
        sv.if %S {
            sv.bpassign %10, %2 : i2
            sv.bpassign %11, %3 : i1
        }
    }
    %8 = sv.read_inout %10 : !hw.inout<i2>
    %9 = sv.read_inout %11 : !hw.inout<i1>
    %12 = hw.struct_create (%8, %9) : !hw.struct<_0: i2, _1: i1>
    hw.output %12 : !hw.struct<_0: i2, _1: i1>
}
