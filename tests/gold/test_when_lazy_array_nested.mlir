module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_lazy_array_nested(%S: i1) -> (O: !hw.array<2x!hw.struct<x: i1, y: i1>>) {
        %0 = hw.constant 0 : i1
        %1 = hw.constant 1 : i1
        %6 = sv.reg name "_WHEN_WIRE_0" : !hw.inout<i1>
        %2 = sv.read_inout %6 : !hw.inout<i1>
        %7 = sv.reg name "_WHEN_WIRE_1" : !hw.inout<i1>
        %3 = sv.read_inout %7 : !hw.inout<i1>
        %8 = sv.reg name "_WHEN_WIRE_2" : !hw.inout<i1>
        %4 = sv.read_inout %8 : !hw.inout<i1>
        %9 = sv.reg name "_WHEN_WIRE_3" : !hw.inout<i1>
        %5 = sv.read_inout %9 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %S {
                sv.bpassign %6, %0 : i1
                sv.bpassign %7, %1 : i1
                sv.bpassign %8, %0 : i1
                sv.bpassign %9, %1 : i1
            } else {
                sv.bpassign %6, %1 : i1
                sv.bpassign %7, %0 : i1
                sv.bpassign %8, %1 : i1
                sv.bpassign %9, %0 : i1
            }
        }
        %10 = hw.struct_create (%2, %3) : !hw.struct<x: i1, y: i1>
        %11 = hw.struct_create (%4, %5) : !hw.struct<x: i1, y: i1>
        %12 = hw.array_create %11, %10 : !hw.struct<x: i1, y: i1>
        %14 = sv.wire sym @test_when_lazy_array_nested.x name "x" : !hw.inout<!hw.array<2x!hw.struct<x: i1, y: i1>>>
        sv.assign %14, %12 : !hw.array<2x!hw.struct<x: i1, y: i1>>
        %13 = sv.read_inout %14 : !hw.inout<!hw.array<2x!hw.struct<x: i1, y: i1>>>
        %15 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %2, %15) : i1, i1, i1
        %16 = hw.constant 1 : i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %3, %16) : i1, i1, i1
        %17 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %4, %17) : i1, i1, i1
        %18 = hw.constant 1 : i1
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %5, %18) : i1, i1, i1
        %20 = hw.constant -1 : i1
        %19 = comb.xor %20, %S : i1
        %21 = hw.constant 1 : i1
        sv.verbatim "WHEN_ASSERT_4: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%19, %2, %21) : i1, i1, i1
        %22 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_5: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%19, %3, %22) : i1, i1, i1
        %23 = hw.constant 1 : i1
        sv.verbatim "WHEN_ASSERT_6: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%19, %4, %23) : i1, i1, i1
        %24 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_7: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%19, %5, %24) : i1, i1, i1
        hw.output %13 : !hw.array<2x!hw.struct<x: i1, y: i1>>
    }
}
