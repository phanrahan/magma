module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @test_when_lazy_array_nested(in %S: i1, out O: !hw.array<2x!hw.struct<x: i1, y: i1>>) {
        %0 = hw.constant 0 : i1
        %1 = hw.constant 1 : i1
        %6 = sv.reg : !hw.inout<i1>
        %2 = sv.read_inout %6 : !hw.inout<i1>
        %7 = sv.reg : !hw.inout<i1>
        %3 = sv.read_inout %7 : !hw.inout<i1>
        %8 = sv.reg : !hw.inout<i1>
        %4 = sv.read_inout %8 : !hw.inout<i1>
        %9 = sv.reg : !hw.inout<i1>
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
        %11 = sv.wire sym @test_when_lazy_array_nested._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i1>
        sv.assign %11, %2 : i1
        %10 = sv.read_inout %11 : !hw.inout<i1>
        %13 = sv.wire sym @test_when_lazy_array_nested._WHEN_ASSERT_1 name "_WHEN_ASSERT_1" : !hw.inout<i1>
        sv.assign %13, %3 : i1
        %12 = sv.read_inout %13 : !hw.inout<i1>
        %14 = hw.struct_create (%10, %12) : !hw.struct<x: i1, y: i1>
        %16 = sv.wire sym @test_when_lazy_array_nested._WHEN_ASSERT_2 name "_WHEN_ASSERT_2" : !hw.inout<i1>
        sv.assign %16, %4 : i1
        %15 = sv.read_inout %16 : !hw.inout<i1>
        %18 = sv.wire sym @test_when_lazy_array_nested._WHEN_ASSERT_3 name "_WHEN_ASSERT_3" : !hw.inout<i1>
        sv.assign %18, %5 : i1
        %17 = sv.read_inout %18 : !hw.inout<i1>
        %19 = hw.struct_create (%15, %17) : !hw.struct<x: i1, y: i1>
        %20 = hw.array_create %19, %14 : !hw.struct<x: i1, y: i1>
        %22 = sv.wire sym @test_when_lazy_array_nested.x name "x" : !hw.inout<!hw.array<2x!hw.struct<x: i1, y: i1>>>
        sv.assign %22, %20 : !hw.array<2x!hw.struct<x: i1, y: i1>>
        %21 = sv.read_inout %22 : !hw.inout<!hw.array<2x!hw.struct<x: i1, y: i1>>>
        %23 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %10, %23) : i1, i1, i1
        %24 = hw.constant 1 : i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %12, %24) : i1, i1, i1
        %25 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %15, %25) : i1, i1, i1
        %26 = hw.constant 1 : i1
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %17, %26) : i1, i1, i1
        %28 = hw.constant -1 : i1
        %27 = comb.xor %28, %S : i1
        %29 = hw.constant 1 : i1
        sv.verbatim "WHEN_ASSERT_4: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%27, %10, %29) : i1, i1, i1
        %30 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_5: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%27, %12, %30) : i1, i1, i1
        %31 = hw.constant 1 : i1
        sv.verbatim "WHEN_ASSERT_6: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%27, %15, %31) : i1, i1, i1
        %32 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_7: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%27, %17, %32) : i1, i1, i1
        hw.output %21 : !hw.array<2x!hw.struct<x: i1, y: i1>>
    }
}
