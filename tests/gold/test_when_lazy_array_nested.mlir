module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_lazy_array_nested(%S: i1) -> (O: !hw.array<2x!hw.struct<x: i1, y: i1>>) {
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
        %10 = hw.struct_create (%2, %3) : !hw.struct<x: i1, y: i1>
        %11 = hw.struct_create (%4, %5) : !hw.struct<x: i1, y: i1>
        %12 = hw.array_create %11, %10 : !hw.struct<x: i1, y: i1>
        %14 = sv.wire sym @test_when_lazy_array_nested.x name "x" : !hw.inout<!hw.array<2x!hw.struct<x: i1, y: i1>>>
        sv.assign %14, %12 : !hw.array<2x!hw.struct<x: i1, y: i1>>
        %13 = sv.read_inout %14 : !hw.inout<!hw.array<2x!hw.struct<x: i1, y: i1>>>
        %16 = sv.wire sym @test_when_lazy_array_nested.x_0_x name "x_0_x" : !hw.inout<i1>
        sv.assign %16, %2 : i1
        %15 = sv.read_inout %16 : !hw.inout<i1>
        %17 = hw.constant 0 : i1
        sv.verbatim "always @(*) WHEN_ASSERT_108: assert (~({{0}}) | ({{1}} == {{2}}));" (%S, %15, %17) : i1, i1, i1
        %19 = sv.wire sym @test_when_lazy_array_nested.x_0_y name "x_0_y" : !hw.inout<i1>
        sv.assign %19, %3 : i1
        %18 = sv.read_inout %19 : !hw.inout<i1>
        %20 = hw.constant 1 : i1
        sv.verbatim "always @(*) WHEN_ASSERT_109: assert (~({{0}}) | ({{1}} == {{2}}));" (%S, %18, %20) : i1, i1, i1
        %22 = sv.wire sym @test_when_lazy_array_nested.x_1_x name "x_1_x" : !hw.inout<i1>
        sv.assign %22, %4 : i1
        %21 = sv.read_inout %22 : !hw.inout<i1>
        %23 = hw.constant 0 : i1
        sv.verbatim "always @(*) WHEN_ASSERT_110: assert (~({{0}}) | ({{1}} == {{2}}));" (%S, %21, %23) : i1, i1, i1
        %25 = sv.wire sym @test_when_lazy_array_nested.x_1_y name "x_1_y" : !hw.inout<i1>
        sv.assign %25, %5 : i1
        %24 = sv.read_inout %25 : !hw.inout<i1>
        %26 = hw.constant 1 : i1
        sv.verbatim "always @(*) WHEN_ASSERT_111: assert (~({{0}}) | ({{1}} == {{2}}));" (%S, %24, %26) : i1, i1, i1
        %28 = hw.constant -1 : i1
        %27 = comb.xor %28, %S : i1
        %29 = hw.constant 1 : i1
        sv.verbatim "always @(*) WHEN_ASSERT_112: assert (~({{0}}) | ({{1}} == {{2}}));" (%27, %15, %29) : i1, i1, i1
        %30 = hw.constant 0 : i1
        sv.verbatim "always @(*) WHEN_ASSERT_113: assert (~({{0}}) | ({{1}} == {{2}}));" (%27, %18, %30) : i1, i1, i1
        %31 = hw.constant 1 : i1
        sv.verbatim "always @(*) WHEN_ASSERT_114: assert (~({{0}}) | ({{1}} == {{2}}));" (%27, %21, %31) : i1, i1, i1
        %32 = hw.constant 0 : i1
        sv.verbatim "always @(*) WHEN_ASSERT_115: assert (~({{0}}) | ({{1}} == {{2}}));" (%27, %24, %32) : i1, i1, i1
        hw.output %13 : !hw.array<2x!hw.struct<x: i1, y: i1>>
    }
}
