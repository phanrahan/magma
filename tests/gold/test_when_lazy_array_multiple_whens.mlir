module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_lazy_array_multiple_whens(%I: i4, %S: i1) -> (O: i4) {
        %1 = hw.constant -1 : i1
        %0 = comb.xor %1, %S : i1
        %3 = sv.reg : !hw.inout<i4>
        %2 = sv.read_inout %3 : !hw.inout<i4>
        sv.alwayscomb {
            sv.if %S {
                %8 = comb.concat %5, %4, %7, %6 : i1, i1, i1, i1
                sv.bpassign %3, %8 : i4
            } else {
                %9 = comb.concat %7, %6, %5, %4 : i1, i1, i1, i1
                sv.bpassign %3, %9 : i4
            }
        }
        %4 = comb.extract %I from 2 : (i4) -> i1
        %5 = comb.extract %I from 3 : (i4) -> i1
        %6 = comb.extract %I from 0 : (i4) -> i1
        %7 = comb.extract %I from 1 : (i4) -> i1
        %10 = comb.extract %2 from 0 : (i4) -> i1
        %11 = comb.extract %I from 0 : (i4) -> i1
        %12 = comb.extract %2 from 1 : (i4) -> i1
        %13 = comb.extract %I from 1 : (i4) -> i1
        %14 = comb.extract %2 from 2 : (i4) -> i1
        %15 = comb.extract %I from 2 : (i4) -> i1
        %16 = comb.extract %2 from 3 : (i4) -> i1
        %17 = comb.extract %I from 3 : (i4) -> i1
        %22 = sv.reg : !hw.inout<i1>
        %18 = sv.read_inout %22 : !hw.inout<i1>
        %23 = sv.reg : !hw.inout<i1>
        %19 = sv.read_inout %23 : !hw.inout<i1>
        %24 = sv.reg : !hw.inout<i1>
        %20 = sv.read_inout %24 : !hw.inout<i1>
        %25 = sv.reg : !hw.inout<i1>
        %21 = sv.read_inout %25 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %22, %10 : i1
            sv.bpassign %23, %12 : i1
            sv.bpassign %24, %14 : i1
            sv.bpassign %25, %16 : i1
            sv.if %0 {
                sv.bpassign %22, %11 : i1
                sv.bpassign %23, %13 : i1
                sv.bpassign %24, %15 : i1
                sv.bpassign %25, %17 : i1
            }
        }
        %26 = comb.concat %21, %20, %19, %18 : i1, i1, i1, i1
        %27 = comb.extract %26 from 0 : (i4) -> i1
        sv.verbatim "always @(*) WHEN_ASSERT_142: assert (~({{0}}) | ({{1}} == {{2}}));" (%0, %27, %11) : i1, i1, i1
        %28 = comb.extract %26 from 1 : (i4) -> i1
        sv.verbatim "always @(*) WHEN_ASSERT_143: assert (~({{0}}) | ({{1}} == {{2}}));" (%0, %28, %13) : i1, i1, i1
        %29 = comb.extract %26 from 2 : (i4) -> i1
        sv.verbatim "always @(*) WHEN_ASSERT_144: assert (~({{0}}) | ({{1}} == {{2}}));" (%0, %29, %15) : i1, i1, i1
        %30 = comb.extract %26 from 3 : (i4) -> i1
        sv.verbatim "always @(*) WHEN_ASSERT_145: assert (~({{0}}) | ({{1}} == {{2}}));" (%0, %30, %17) : i1, i1, i1
        %31 = comb.xor %1, %0 : i1
        sv.verbatim "always @(*) WHEN_ASSERT_146: assert (~({{0}}) | ({{1}} == {{2}}));" (%31, %27, %10) : i1, i1, i1
        sv.verbatim "always @(*) WHEN_ASSERT_147: assert (~({{0}}) | ({{1}} == {{2}}));" (%31, %28, %12) : i1, i1, i1
        sv.verbatim "always @(*) WHEN_ASSERT_148: assert (~({{0}}) | ({{1}} == {{2}}));" (%31, %29, %14) : i1, i1, i1
        sv.verbatim "always @(*) WHEN_ASSERT_149: assert (~({{0}}) | ({{1}} == {{2}}));" (%31, %30, %16) : i1, i1, i1
        sv.verbatim "always @(*) WHEN_ASSERT_150: assert (~({{0}}) | ({{1}} == {{2}}));" (%S, %29, %15) : i1, i1, i1
        sv.verbatim "always @(*) WHEN_ASSERT_151: assert (~({{0}}) | ({{1}} == {{2}}));" (%S, %30, %17) : i1, i1, i1
        sv.verbatim "always @(*) WHEN_ASSERT_152: assert (~({{0}}) | ({{1}} == {{2}}));" (%S, %27, %11) : i1, i1, i1
        sv.verbatim "always @(*) WHEN_ASSERT_153: assert (~({{0}}) | ({{1}} == {{2}}));" (%S, %28, %13) : i1, i1, i1
        %32 = comb.xor %1, %S : i1
        sv.verbatim "always @(*) WHEN_ASSERT_154: assert (~({{0}}) | ({{1}} == {{2}}));" (%32, %29, %11) : i1, i1, i1
        sv.verbatim "always @(*) WHEN_ASSERT_155: assert (~({{0}}) | ({{1}} == {{2}}));" (%32, %30, %13) : i1, i1, i1
        sv.verbatim "always @(*) WHEN_ASSERT_156: assert (~({{0}}) | ({{1}} == {{2}}));" (%32, %27, %15) : i1, i1, i1
        sv.verbatim "always @(*) WHEN_ASSERT_157: assert (~({{0}}) | ({{1}} == {{2}}));" (%32, %28, %17) : i1, i1, i1
        hw.output %26 : i4
    }
}
