module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_lazy_array(%S: i1) -> (O: i2) {
        %0 = hw.constant 0 : i1
        %1 = hw.constant 1 : i1
        %4 = sv.reg : !hw.inout<i1>
        %2 = sv.read_inout %4 : !hw.inout<i1>
        %5 = sv.reg : !hw.inout<i1>
        %3 = sv.read_inout %5 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %S {
                sv.bpassign %4, %0 : i1
                sv.bpassign %5, %1 : i1
            } else {
                sv.bpassign %4, %1 : i1
                sv.bpassign %5, %0 : i1
            }
        }
        %6 = comb.concat %3, %2 : i1, i1
        %8 = sv.wire sym @test_when_lazy_array.x name "x" : !hw.inout<i2>
        sv.assign %8, %6 : i2
        %7 = sv.read_inout %8 : !hw.inout<i2>
        %9 = comb.extract %7 from 0 : (i2) -> i1
        %10 = hw.constant 0 : i1
        sv.verbatim "always @(*) WHEN_ASSERT_96: assert (~({{0}}) | ({{1}} == {{2}}));" (%S, %9, %10) : i1, i1, i1
        %11 = comb.extract %7 from 1 : (i2) -> i1
        %12 = hw.constant 1 : i1
        sv.verbatim "always @(*) WHEN_ASSERT_97: assert (~({{0}}) | ({{1}} == {{2}}));" (%S, %11, %12) : i1, i1, i1
        %14 = hw.constant -1 : i1
        %13 = comb.xor %14, %S : i1
        %15 = hw.constant 1 : i1
        sv.verbatim "always @(*) WHEN_ASSERT_98: assert (~({{0}}) | ({{1}} == {{2}}));" (%13, %9, %15) : i1, i1, i1
        %16 = hw.constant 0 : i1
        sv.verbatim "always @(*) WHEN_ASSERT_99: assert (~({{0}}) | ({{1}} == {{2}}));" (%13, %11, %16) : i1, i1, i1
        hw.output %7 : i2
    }
}
