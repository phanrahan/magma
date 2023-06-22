module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_array_3d_bulk_child(%I: !hw.array<2x!hw.array<2xi2>>, %S: i1) -> (O: !hw.array<2x!hw.array<2xi2>>) {
        %1 = sv.reg name "_WHEN_WIRE_129" : !hw.inout<!hw.array<2x!hw.array<2xi2>>>
        %0 = sv.read_inout %1 : !hw.inout<!hw.array<2x!hw.array<2xi2>>>
        sv.alwayscomb {
            sv.if %S {
                %11 = hw.array_create %6, %4 : i2
                %12 = hw.array_create %9, %8 : i2
                %10 = hw.array_create %12, %11 : !hw.array<2xi2>
                sv.bpassign %1, %10 : !hw.array<2x!hw.array<2xi2>>
            } else {
                %14 = hw.array_create %9, %8 : i2
                %15 = hw.array_create %6, %4 : i2
                %13 = hw.array_create %15, %14 : !hw.array<2xi2>
                sv.bpassign %1, %13 : !hw.array<2x!hw.array<2xi2>>
            }
        }
        %2 = hw.constant 0 : i1
        %3 = hw.array_get %I[%2] : !hw.array<2x!hw.array<2xi2>>, i1
        %4 = hw.array_get %3[%2] : !hw.array<2xi2>, i1
        %5 = hw.constant 1 : i1
        %6 = hw.array_get %3[%5] : !hw.array<2xi2>, i1
        %7 = hw.array_get %I[%5] : !hw.array<2x!hw.array<2xi2>>, i1
        %8 = hw.array_get %7[%2] : !hw.array<2xi2>, i1
        %9 = hw.array_get %7[%5] : !hw.array<2xi2>, i1
        %16 = hw.array_get %0[%2] : !hw.array<2x!hw.array<2xi2>>, i1
        %17 = hw.array_get %16[%5] : !hw.array<2xi2>, i1
        %18 = hw.array_get %16[%2] : !hw.array<2xi2>, i1
        %19 = hw.array_get %I[%2] : !hw.array<2x!hw.array<2xi2>>, i1
        %20 = hw.array_get %19[%5] : !hw.array<2xi2>, i1
        %21 = hw.array_get %19[%2] : !hw.array<2xi2>, i1
        sv.verbatim "WHEN_ASSERT_287: assert property (({{0}}) |-> ({{{1}}, {{2}}} == {{{3}}, {{4}}}));" (%S, %17, %18, %20, %21) : i1, i2, i2, i2, i2
        %22 = hw.array_get %0[%5] : !hw.array<2x!hw.array<2xi2>>, i1
        %23 = hw.array_get %22[%5] : !hw.array<2xi2>, i1
        %24 = hw.array_get %22[%2] : !hw.array<2xi2>, i1
        %25 = hw.array_get %I[%5] : !hw.array<2x!hw.array<2xi2>>, i1
        %26 = hw.array_get %25[%5] : !hw.array<2xi2>, i1
        %27 = hw.array_get %25[%2] : !hw.array<2xi2>, i1
        sv.verbatim "WHEN_ASSERT_288: assert property (({{0}}) |-> ({{{1}}, {{2}}} == {{{3}}, {{4}}}));" (%S, %23, %24, %26, %27) : i1, i2, i2, i2, i2
        %29 = hw.constant -1 : i1
        %28 = comb.xor %29, %S : i1
        sv.verbatim "WHEN_ASSERT_289: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%28, %18, %27) : i1, i2, i2
        sv.verbatim "WHEN_ASSERT_290: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%28, %17, %26) : i1, i2, i2
        sv.verbatim "WHEN_ASSERT_291: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%28, %24, %21) : i1, i2, i2
        sv.verbatim "WHEN_ASSERT_292: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%28, %23, %20) : i1, i2, i2
        hw.output %0 : !hw.array<2x!hw.array<2xi2>>
    }
}
