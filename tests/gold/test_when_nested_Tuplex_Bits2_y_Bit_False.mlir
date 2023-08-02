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
        %12 = hw.struct_extract %4["x"] : !hw.struct<x: i2, y: i1>
        %14 = sv.wire sym @test_when_nested_Tuplex_Bits2_y_Bit_False._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i2>
        sv.assign %14, %12 : i2
        %13 = sv.read_inout %14 : !hw.inout<i2>
        %15 = hw.struct_extract %4["y"] : !hw.struct<x: i2, y: i1>
        %17 = sv.wire sym @test_when_nested_Tuplex_Bits2_y_Bit_False._WHEN_ASSERT_1 name "_WHEN_ASSERT_1" : !hw.inout<i1>
        sv.assign %17, %15 : i1
        %16 = sv.read_inout %17 : !hw.inout<i1>
        %18 = hw.struct_create (%13, %16) : !hw.struct<x: i2, y: i1>
        %19 = hw.struct_extract %2["x"] : !hw.struct<x: i2, y: i1>
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %13, %19) : i1, i2, i2
        %20 = hw.struct_extract %2["y"] : !hw.struct<x: i2, y: i1>
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %16, %20) : i1, i1, i1
        %22 = hw.constant -1 : i1
        %21 = comb.xor %22, %S : i1
        %23 = hw.struct_extract %0["x"] : !hw.struct<x: i2, y: i1>
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%21, %13, %23) : i1, i2, i2
        %24 = comb.xor %22, %S : i1
        %25 = hw.struct_extract %0["y"] : !hw.struct<x: i2, y: i1>
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%24, %16, %25) : i1, i1, i1
        hw.output %18 : !hw.struct<x: i2, y: i1>
    }
}
