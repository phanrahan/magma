module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_2d_array_assign_slice(%I: !hw.array<4xi2>, %S: i1) -> (O: !hw.array<4xi2>) {
        %1 = sv.reg : !hw.inout<!hw.array<4xi2>>
        %0 = sv.read_inout %1 : !hw.inout<!hw.array<4xi2>>
        sv.alwayscomb {
            sv.if %S {
                %10 = hw.array_create %5, %3, %9, %7 : i2
                sv.bpassign %1, %10 : !hw.array<4xi2>
            } else {
                %11 = hw.array_create %9, %7, %5, %3 : i2
                sv.bpassign %1, %11 : !hw.array<4xi2>
            }
        }
        %2 = hw.constant 2 : i2
        %3 = hw.array_get %I[%2] : !hw.array<4xi2>, i2
        %4 = hw.constant 3 : i2
        %5 = hw.array_get %I[%4] : !hw.array<4xi2>, i2
        %6 = hw.constant 0 : i2
        %7 = hw.array_get %I[%6] : !hw.array<4xi2>, i2
        %8 = hw.constant 1 : i2
        %9 = hw.array_get %I[%8] : !hw.array<4xi2>, i2
        %12 = hw.array_get %I[%8] : !hw.array<4xi2>, i2
        %13 = hw.array_get %I[%6] : !hw.array<4xi2>, i2
        %14 = hw.array_get %0[%8] : !hw.array<4xi2>, i2
        %15 = hw.array_get %0[%6] : !hw.array<4xi2>, i2
        sv.verbatim "always @(*) WHEN_ASSERT_344: assert (~({{0}}) | ('{{{1}}, {{2}}} == '{{{3}}, {{4}}}));" (%S, %14, %15, %12, %13) : i1, i2, i2, i2, i2
        %16 = hw.array_get %I[%2] : !hw.array<4xi2>, i2
        %17 = hw.array_get %0[%2] : !hw.array<4xi2>, i2
        sv.verbatim "always @(*) WHEN_ASSERT_345: assert (~({{0}}) | ({{1}} == {{2}}));" (%S, %17, %16) : i1, i2, i2
        %18 = hw.array_get %I[%4] : !hw.array<4xi2>, i2
        %19 = hw.array_get %0[%4] : !hw.array<4xi2>, i2
        sv.verbatim "always @(*) WHEN_ASSERT_346: assert (~({{0}}) | ({{1}} == {{2}}));" (%S, %19, %18) : i1, i2, i2
        %21 = hw.constant -1 : i1
        %20 = comb.xor %21, %S : i1
        sv.verbatim "always @(*) WHEN_ASSERT_347: assert (~({{0}}) | ({{1}} == {{2}}));" (%20, %17, %13) : i1, i2, i2
        sv.verbatim "always @(*) WHEN_ASSERT_348: assert (~({{0}}) | ({{1}} == {{2}}));" (%20, %19, %12) : i1, i2, i2
        sv.verbatim "always @(*) WHEN_ASSERT_349: assert (~({{0}}) | ({{1}} == {{2}}));" (%20, %15, %16) : i1, i2, i2
        sv.verbatim "always @(*) WHEN_ASSERT_350: assert (~({{0}}) | ({{1}} == {{2}}));" (%20, %14, %18) : i1, i2, i2
        hw.output %0 : !hw.array<4xi2>
    }
}
