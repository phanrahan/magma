module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_3d_array_assign(%I: !hw.array<2x!hw.array<2xi2>>, %S: i1) -> (O: !hw.array<2x!hw.array<2xi2>>) {
        %1 = sv.reg name "_WHEN_WIRE_127" : !hw.inout<!hw.array<2x!hw.array<2xi2>>>
        %0 = sv.read_inout %1 : !hw.inout<!hw.array<2x!hw.array<2xi2>>>
        sv.alwayscomb {
            sv.if %S {
                %11 = hw.array_create %9, %8 : i2
                %12 = hw.array_create %6, %5 : i2
                %10 = hw.array_create %12, %11 : !hw.array<2xi2>
                sv.bpassign %1, %10 : !hw.array<2x!hw.array<2xi2>>
            } else {
                %14 = hw.array_create %5, %6 : i2
                %15 = hw.array_create %8, %9 : i2
                %13 = hw.array_create %15, %14 : !hw.array<2xi2>
                sv.bpassign %1, %13 : !hw.array<2x!hw.array<2xi2>>
            }
        }
        %2 = hw.constant 1 : i1
        %3 = hw.array_get %I[%2] : !hw.array<2x!hw.array<2xi2>>, i1
        %4 = hw.constant 0 : i1
        %5 = hw.array_get %3[%4] : !hw.array<2xi2>, i1
        %6 = hw.array_get %3[%2] : !hw.array<2xi2>, i1
        %7 = hw.array_get %I[%4] : !hw.array<2x!hw.array<2xi2>>, i1
        %8 = hw.array_get %7[%4] : !hw.array<2xi2>, i1
        %9 = hw.array_get %7[%2] : !hw.array<2xi2>, i1
        %16 = hw.array_get %0[%2] : !hw.array<2x!hw.array<2xi2>>, i1
        %17 = hw.array_get %16[%4] : !hw.array<2xi2>, i1
        %18 = hw.array_get %I[%2] : !hw.array<2x!hw.array<2xi2>>, i1
        %19 = hw.array_get %18[%4] : !hw.array<2xi2>, i1
        sv.verbatim "WHEN_ASSERT_263: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %17, %19) : i1, i2, i2
        %20 = hw.array_get %16[%2] : !hw.array<2xi2>, i1
        %21 = hw.array_get %18[%2] : !hw.array<2xi2>, i1
        sv.verbatim "WHEN_ASSERT_264: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %20, %21) : i1, i2, i2
        %22 = hw.array_get %0[%4] : !hw.array<2x!hw.array<2xi2>>, i1
        %23 = hw.array_get %22[%4] : !hw.array<2xi2>, i1
        %24 = hw.array_get %I[%4] : !hw.array<2x!hw.array<2xi2>>, i1
        %25 = hw.array_get %24[%4] : !hw.array<2xi2>, i1
        sv.verbatim "WHEN_ASSERT_265: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %23, %25) : i1, i2, i2
        %26 = hw.array_get %22[%2] : !hw.array<2xi2>, i1
        %27 = hw.array_get %24[%2] : !hw.array<2xi2>, i1
        sv.verbatim "WHEN_ASSERT_266: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %26, %27) : i1, i2, i2
        %29 = hw.constant -1 : i1
        %28 = comb.xor %29, %S : i1
        sv.verbatim "WHEN_ASSERT_267: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%28, %17, %27) : i1, i2, i2
        sv.verbatim "WHEN_ASSERT_268: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%28, %20, %25) : i1, i2, i2
        sv.verbatim "WHEN_ASSERT_269: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%28, %23, %21) : i1, i2, i2
        sv.verbatim "WHEN_ASSERT_270: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%28, %26, %19) : i1, i2, i2
        hw.output %0 : !hw.array<2x!hw.array<2xi2>>
    }
}
