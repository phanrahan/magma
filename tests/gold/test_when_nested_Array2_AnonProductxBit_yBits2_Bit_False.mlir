module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_nested_Array2_AnonProductxBit_yBits2_Bit_False(%I: !hw.array<2x!hw.array<2x!hw.struct<x: i1, y: i2>>>, %S: i1) -> (O: !hw.array<2x!hw.struct<x: i1, y: i2>>) {
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
        %15 = hw.struct_extract %14["y"] : !hw.struct<x: i1, y: i2>
        %16 = hw.struct_extract %14["x"] : !hw.struct<x: i1, y: i2>
        %17 = hw.array_get %12[%3] : !hw.array<2x!hw.struct<x: i1, y: i2>>, i1
        %18 = hw.struct_extract %17["y"] : !hw.struct<x: i1, y: i2>
        %19 = hw.struct_extract %17["x"] : !hw.struct<x: i1, y: i2>
        %20 = hw.array_get %2[%1] : !hw.array<2x!hw.struct<x: i1, y: i2>>, i1
        %21 = hw.struct_extract %20["y"] : !hw.struct<x: i1, y: i2>
        %22 = hw.struct_extract %20["x"] : !hw.struct<x: i1, y: i2>
        %23 = hw.array_get %2[%3] : !hw.array<2x!hw.struct<x: i1, y: i2>>, i1
        %24 = hw.struct_extract %23["y"] : !hw.struct<x: i1, y: i2>
        %25 = hw.struct_extract %23["x"] : !hw.struct<x: i1, y: i2>
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{{{1}}, {{2}}}, {{{3}}, {{4}}}} == {{{{5}}, {{6}}}, {{{7}}, {{8}}}}));" (%S, %15, %16, %18, %19, %21, %22, %24, %25) : i1, i2, i1, i2, i1, i2, i1, i2, i1
        hw.output %4 : !hw.array<2x!hw.struct<x: i1, y: i2>>
    }
}
