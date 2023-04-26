module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_lazy_array_protocol(%S: i1) -> (O: !hw.array<2xi1>) {
        %0 = hw.constant 0 : i1
        %1 = hw.constant 1 : i1
        %4 = sv.reg : !hw.inout<i1>
        %2 = sv.read_inout %4 : !hw.inout<i1>
        %5 = sv.reg : !hw.inout<i1>
        %3 = sv.read_inout %5 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %S {
                sv.bpassign %4, %0 : i1
                sv.bpassign %5, %0 : i1
            } else {
                sv.bpassign %4, %1 : i1
                sv.bpassign %5, %1 : i1
            }
        }
        %6 = hw.array_create %3, %2 : i1
        %8 = sv.wire sym @test_when_lazy_array_protocol.x name "x" : !hw.inout<!hw.array<2xi1>>
        sv.assign %8, %6 : !hw.array<2xi1>
        %7 = sv.read_inout %8 : !hw.inout<!hw.array<2xi1>>
        %10 = hw.constant 0 : i1
        %9 = hw.array_get %7[%10] : !hw.array<2xi1>, i1
        %11 = hw.constant 0 : i1
        sv.verbatim "always @(*) WHEN_ASSERT_116: assert (~({{0}}) | ({{1}} == {{2}}));" (%S, %9, %11) : i1, i1, i1
        %13 = hw.constant 1 : i1
        %12 = hw.array_get %7[%13] : !hw.array<2xi1>, i1
        %14 = hw.constant 0 : i1
        sv.verbatim "always @(*) WHEN_ASSERT_117: assert (~({{0}}) | ({{1}} == {{2}}));" (%S, %12, %14) : i1, i1, i1
        %16 = hw.constant -1 : i1
        %15 = comb.xor %16, %S : i1
        %17 = hw.constant 1 : i1
        sv.verbatim "always @(*) WHEN_ASSERT_118: assert (~({{0}}) | ({{1}} == {{2}}));" (%15, %9, %17) : i1, i1, i1
        %18 = hw.constant 1 : i1
        sv.verbatim "always @(*) WHEN_ASSERT_119: assert (~({{0}}) | ({{1}} == {{2}}));" (%15, %12, %18) : i1, i1, i1
        hw.output %7 : !hw.array<2xi1>
    }
}
