module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @test_when_nested_Tuplex_Bits2_y_Bit_False(in %I: !hw.array<2x!hw.struct<x: i2, y: i1>>, in %S: i1, out O: !hw.struct<x: i2, y: i1>) {
        %1 = hw.constant 1 : i1
        %0 = hw.array_get %I[%1] : !hw.array<2x!hw.struct<x: i2, y: i1>>, i1
        %3 = hw.constant 0 : i1
        %2 = hw.array_get %I[%3] : !hw.array<2x!hw.struct<x: i2, y: i1>>, i1
        %5 = sv.reg : !hw.inout<!hw.struct<x: i2, y: i1>>
        %4 = sv.read_inout %5 : !hw.inout<!hw.struct<x: i2, y: i1>>
        sv.alwayscomb {
            sv.bpassign %5, %0 : !hw.struct<x: i2, y: i1>
            sv.if %S {
                sv.bpassign %5, %2 : !hw.struct<x: i2, y: i1>
            }
        }
        %7 = sv.wire sym @test_when_nested_Tuplex_Bits2_y_Bit_False._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<!hw.struct<x: i2, y: i1>>
        sv.assign %7, %4 : !hw.struct<x: i2, y: i1>
        %6 = sv.read_inout %7 : !hw.inout<!hw.struct<x: i2, y: i1>>
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %6, %2) : i1, !hw.struct<x: i2, y: i1>, !hw.struct<x: i2, y: i1>
        %9 = hw.constant -1 : i1
        %8 = comb.xor %9, %S : i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%8, %6, %0) : i1, !hw.struct<x: i2, y: i1>, !hw.struct<x: i2, y: i1>
        hw.output %6 : !hw.struct<x: i2, y: i1>
    }
}
