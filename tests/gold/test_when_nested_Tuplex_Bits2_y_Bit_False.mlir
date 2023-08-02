module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_nested_Tuplex_Bits2_y_Bit_False(%I: !hw.array<2x!hw.struct<x: i2, y: i1>>, %S: i1) -> (O: !hw.struct<x: i2, y: i1>) {
        %1 = hw.constant 1 : i1
        %0 = hw.array_get %I[%1] : !hw.array<2x!hw.struct<x: i2, y: i1>>, i1
        %3 = hw.constant 0 : i1
        %2 = hw.array_get %I[%3] : !hw.array<2x!hw.struct<x: i2, y: i1>>, i1
        %5 = sv.reg : !hw.inout<!hw.struct<x: i2, y: i1>>
        %4 = sv.read_inout %5 : !hw.inout<!hw.struct<x: i2, y: i1>>
        sv.alwayscomb {
            %8 = hw.struct_create (%6, %7) : !hw.struct<x: i2, y: i1>
            sv.bpassign %5, %8 : !hw.struct<x: i2, y: i1>
            sv.if %S {
                %11 = hw.struct_create (%9, %10) : !hw.struct<x: i2, y: i1>
                sv.bpassign %5, %11 : !hw.struct<x: i2, y: i1>
            }
        }
        %6 = hw.struct_extract %0["x"] : !hw.struct<x: i2, y: i1>
        %7 = hw.struct_extract %0["y"] : !hw.struct<x: i2, y: i1>
        %9 = hw.struct_extract %2["x"] : !hw.struct<x: i2, y: i1>
        %10 = hw.struct_extract %2["y"] : !hw.struct<x: i2, y: i1>
        %13 = sv.wire sym @test_when_nested_Tuplex_Bits2_y_Bit_False._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<!hw.struct<x: i2, y: i1>>
        sv.assign %13, %4 : !hw.struct<x: i2, y: i1>
        %12 = sv.read_inout %13 : !hw.inout<!hw.struct<x: i2, y: i1>>
        %14 = hw.struct_extract %12["y"] : !hw.struct<x: i2, y: i1>
        %15 = hw.struct_extract %12["x"] : !hw.struct<x: i2, y: i1>
        %16 = hw.struct_extract %2["y"] : !hw.struct<x: i2, y: i1>
        %17 = hw.struct_extract %2["x"] : !hw.struct<x: i2, y: i1>
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{{1}}, {{2}}} == {{{3}}, {{4}}}));" (%S, %14, %15, %16, %17) : i1, i1, i2, i1, i2
        hw.output %4 : !hw.struct<x: i2, y: i1>
    }
}
