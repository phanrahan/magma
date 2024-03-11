module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @test_when_nested_Array2_AnonProductxBit_yBits2_Bit_False(in %I: !hw.array<2x!hw.array<2x!hw.struct<x: i1, y: i2>>>, in %S: i1, out O: !hw.array<2x!hw.struct<x: i1, y: i2>>) {
        %1 = hw.constant 1 : i1
        %0 = hw.array_get %I[%1] : !hw.array<2x!hw.array<2x!hw.struct<x: i1, y: i2>>>, i1
        %3 = hw.constant 0 : i1
        %2 = hw.array_get %I[%3] : !hw.array<2x!hw.array<2x!hw.struct<x: i1, y: i2>>>, i1
        %5 = sv.reg : !hw.inout<!hw.array<2x!hw.struct<x: i1, y: i2>>>
        %4 = sv.read_inout %5 : !hw.inout<!hw.array<2x!hw.struct<x: i1, y: i2>>>
        sv.alwayscomb {
            %8 = hw.array_create %7, %6 : !hw.struct<x: i1, y: i2>
            sv.bpassign %5, %8 : !hw.array<2x!hw.struct<x: i1, y: i2>>
            sv.if %S {
                %11 = hw.array_create %10, %9 : !hw.struct<x: i1, y: i2>
                sv.bpassign %5, %11 : !hw.array<2x!hw.struct<x: i1, y: i2>>
            }
        }
        %6 = hw.array_get %0[%3] : !hw.array<2x!hw.struct<x: i1, y: i2>>, i1
        %7 = hw.array_get %0[%1] : !hw.array<2x!hw.struct<x: i1, y: i2>>, i1
        %9 = hw.array_get %2[%3] : !hw.array<2x!hw.struct<x: i1, y: i2>>, i1
        %10 = hw.array_get %2[%1] : !hw.array<2x!hw.struct<x: i1, y: i2>>, i1
        %13 = sv.wire sym @test_when_nested_Array2_AnonProductxBit_yBits2_Bit_False._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<!hw.array<2x!hw.struct<x: i1, y: i2>>>
        sv.assign %13, %4 : !hw.array<2x!hw.struct<x: i1, y: i2>>
        %12 = sv.read_inout %13 : !hw.inout<!hw.array<2x!hw.struct<x: i1, y: i2>>>
        %14 = hw.array_get %12[%1] : !hw.array<2x!hw.struct<x: i1, y: i2>>, i1
        %15 = hw.array_get %12[%3] : !hw.array<2x!hw.struct<x: i1, y: i2>>, i1
        %16 = hw.array_get %2[%1] : !hw.array<2x!hw.struct<x: i1, y: i2>>, i1
        %17 = hw.array_get %2[%3] : !hw.array<2x!hw.struct<x: i1, y: i2>>, i1
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{{1}}, {{2}}} == {{{3}}, {{4}}}));" (%S, %14, %15, %16, %17) : i1, !hw.struct<x: i1, y: i2>, !hw.struct<x: i1, y: i2>, !hw.struct<x: i1, y: i2>, !hw.struct<x: i1, y: i2>
        hw.output %4 : !hw.array<2x!hw.struct<x: i1, y: i2>>
    }
}
