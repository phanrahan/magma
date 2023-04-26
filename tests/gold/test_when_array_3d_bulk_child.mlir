module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_array_3d_bulk_child(%I: !hw.array<2x!hw.array<2xi2>>, %S: i1) -> (O: !hw.array<2x!hw.array<2xi2>>) {
        %1 = sv.reg : !hw.inout<!hw.array<2x!hw.array<2xi2>>>
        %0 = sv.read_inout %1 : !hw.inout<!hw.array<2x!hw.array<2xi2>>>
        sv.alwayscomb {
            sv.if %S {
                %6 = hw.array_create %5, %3 : !hw.array<2xi2>
                sv.bpassign %1, %6 : !hw.array<2x!hw.array<2xi2>>
            } else {
                %7 = hw.array_create %3, %5 : !hw.array<2xi2>
                sv.bpassign %1, %7 : !hw.array<2x!hw.array<2xi2>>
            }
        }
        %2 = hw.constant 0 : i1
        %3 = hw.array_get %I[%2] : !hw.array<2x!hw.array<2xi2>>, i1
        %4 = hw.constant 1 : i1
        %5 = hw.array_get %I[%4] : !hw.array<2x!hw.array<2xi2>>, i1
        %8 = hw.array_get %I[%2] : !hw.array<2x!hw.array<2xi2>>, i1
        %9 = hw.array_get %8[%4] : !hw.array<2xi2>, i1
        %10 = hw.array_get %8[%2] : !hw.array<2xi2>, i1
        sv.verbatim "always @(*) WHEN_ASSERT_316: assert (~({{0}}) | ('{{{1}}, {{2}}} == '{{{3}}, {{4}}}));" (%S, %11, %12, %9, %10) : i1, i2, i2, i2, i2
        %13 = hw.array_get %I[%4] : !hw.array<2x!hw.array<2xi2>>, i1
        %14 = hw.array_get %13[%4] : !hw.array<2xi2>, i1
        %15 = hw.array_get %13[%2] : !hw.array<2xi2>, i1
        sv.verbatim "always @(*) WHEN_ASSERT_317: assert (~({{0}}) | ('{{{1}}, {{2}}} == '{{{3}}, {{4}}}));" (%S, %16, %17, %14, %15) : i1, i2, i2, i2, i2
        %19 = hw.constant -1 : i1
        %18 = comb.xor %19, %S : i1
        sv.verbatim "always @(*) WHEN_ASSERT_318: assert (~({{0}}) | ('{{{1}}, {{2}}} == '{{{3}}, {{4}}}));" (%18, %16, %17, %9, %10) : i1, i2, i2, i2, i2
        sv.verbatim "always @(*) WHEN_ASSERT_319: assert (~({{0}}) | ('{{{1}}, {{2}}} == '{{{3}}, {{4}}}));" (%18, %11, %12, %14, %15) : i1, i2, i2, i2, i2
        hw.output %0 : !hw.array<2x!hw.array<2xi2>>
    }
}
