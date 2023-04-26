module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_2d_array_assign(%I: !hw.array<2xi2>, %S: i1) -> (O: !hw.array<2xi2>) {
        %1 = sv.reg : !hw.inout<!hw.array<2xi2>>
        %0 = sv.read_inout %1 : !hw.inout<!hw.array<2xi2>>
        sv.alwayscomb {
            sv.if %S {
                %6 = hw.array_create %5, %3 : i2
                sv.bpassign %1, %6 : !hw.array<2xi2>
            } else {
                %7 = hw.array_create %3, %5 : i2
                sv.bpassign %1, %7 : !hw.array<2xi2>
            }
        }
        %2 = hw.constant 0 : i1
        %3 = hw.array_get %I[%2] : !hw.array<2xi2>, i1
        %4 = hw.constant 1 : i1
        %5 = hw.array_get %I[%4] : !hw.array<2xi2>, i1
        %8 = hw.array_get %I[%2] : !hw.array<2xi2>, i1
        sv.verbatim "always @(*) WHEN_ASSERT_256: assert (~({{0}}) | ({{1}} == {{2}}));" (%S, %9, %8) : i1, i2, i2
        %10 = hw.array_get %I[%4] : !hw.array<2xi2>, i1
        sv.verbatim "always @(*) WHEN_ASSERT_257: assert (~({{0}}) | ({{1}} == {{2}}));" (%S, %11, %10) : i1, i2, i2
        %13 = hw.constant -1 : i1
        %12 = comb.xor %13, %S : i1
        sv.verbatim "always @(*) WHEN_ASSERT_258: assert (~({{0}}) | ({{1}} == {{2}}));" (%12, %9, %10) : i1, i2, i2
        sv.verbatim "always @(*) WHEN_ASSERT_259: assert (~({{0}}) | ({{1}} == {{2}}));" (%12, %11, %8) : i1, i2, i2
        hw.output %0 : !hw.array<2xi2>
    }
}
