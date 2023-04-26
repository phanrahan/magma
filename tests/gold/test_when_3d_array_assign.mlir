module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_3d_array_assign(%I: !hw.array<2x!hw.array<2xi2>>, %S: i1) -> (O: !hw.array<2x!hw.array<2xi2>>) {
        %1 = sv.reg : !hw.inout<!hw.array<2x!hw.array<2xi2>>>
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
        %16 = hw.array_get %I[%2] : !hw.array<2x!hw.array<2xi2>>, i1
        %17 = hw.array_get %16[%4] : !hw.array<2xi2>, i1
        %18 = hw.array_get %0[%4] : !hw.array<2x!hw.array<2xi2>>, i1
        %19 = hw.array_get %18[%2] : !hw.array<2xi2>, i1
        sv.verbatim "always @(*) WHEN_ASSERT_292: assert (~({{0}}) | ({{1}} == {{2}}));" (%S, %19, %17) : i1, i2, i2
        %20 = hw.array_get %16[%2] : !hw.array<2xi2>, i1
        %21 = hw.array_get %0[%2] : !hw.array<2x!hw.array<2xi2>>, i1
        %22 = hw.array_get %21[%2] : !hw.array<2xi2>, i1
        sv.verbatim "always @(*) WHEN_ASSERT_293: assert (~({{0}}) | ({{1}} == {{2}}));" (%S, %22, %20) : i1, i2, i2
        %23 = hw.array_get %I[%4] : !hw.array<2x!hw.array<2xi2>>, i1
        %24 = hw.array_get %23[%4] : !hw.array<2xi2>, i1
        %25 = hw.array_get %18[%4] : !hw.array<2xi2>, i1
        sv.verbatim "always @(*) WHEN_ASSERT_294: assert (~({{0}}) | ({{1}} == {{2}}));" (%S, %25, %24) : i1, i2, i2
        %26 = hw.array_get %23[%2] : !hw.array<2xi2>, i1
        %27 = hw.array_get %21[%4] : !hw.array<2xi2>, i1
        sv.verbatim "always @(*) WHEN_ASSERT_295: assert (~({{0}}) | ({{1}} == {{2}}));" (%S, %27, %26) : i1, i2, i2
        %29 = hw.constant -1 : i1
        %28 = comb.xor %29, %S : i1
        sv.verbatim "always @(*) WHEN_ASSERT_296: assert (~({{0}}) | ({{1}} == {{2}}));" (%28, %19, %26) : i1, i2, i2
        sv.verbatim "always @(*) WHEN_ASSERT_297: assert (~({{0}}) | ({{1}} == {{2}}));" (%28, %22, %24) : i1, i2, i2
        sv.verbatim "always @(*) WHEN_ASSERT_298: assert (~({{0}}) | ({{1}} == {{2}}));" (%28, %25, %20) : i1, i2, i2
        sv.verbatim "always @(*) WHEN_ASSERT_299: assert (~({{0}}) | ({{1}} == {{2}}));" (%28, %27, %17) : i1, i2, i2
        hw.output %0 : !hw.array<2x!hw.array<2xi2>>
    }
}
