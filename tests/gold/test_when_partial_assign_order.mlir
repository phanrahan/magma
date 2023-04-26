module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_partial_assign_order(%I: i2, %S: i2) -> (O0: i2, O1: i2, O2: i2) {
        %0 = comb.extract %S from 0 : (i2) -> i1
        %2 = hw.constant -1 : i2
        %1 = comb.xor %2, %I : i2
        %3 = comb.extract %1 from 1 : (i2) -> i1
        %4 = comb.extract %1 from 0 : (i2) -> i1
        %5 = comb.extract %S from 1 : (i2) -> i1
        %6 = comb.xor %2, %I : i2
        %7 = comb.extract %6 from 0 : (i2) -> i1
        %8 = comb.extract %6 from 1 : (i2) -> i1
        %9 = comb.xor %2, %I : i2
        %10 = comb.extract %9 from 0 : (i2) -> i1
        %11 = comb.extract %9 from 1 : (i2) -> i1
        %17 = sv.reg : !hw.inout<i1>
        %12 = sv.read_inout %17 : !hw.inout<i1>
        %18 = sv.reg : !hw.inout<i1>
        %13 = sv.read_inout %18 : !hw.inout<i1>
        %19 = sv.reg : !hw.inout<i2>
        %14 = sv.read_inout %19 : !hw.inout<i2>
        %20 = sv.reg : !hw.inout<i1>
        %15 = sv.read_inout %20 : !hw.inout<i1>
        %21 = sv.reg : !hw.inout<i1>
        %16 = sv.read_inout %21 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %20, %22 : i1
            sv.bpassign %21, %23 : i1
            sv.if %0 {
                sv.bpassign %17, %3 : i1
                sv.bpassign %18, %4 : i1
                %24 = comb.concat %23, %22 : i1, i1
                sv.bpassign %19, %24 : i2
            } else {
                sv.if %5 {
                    sv.bpassign %17, %22 : i1
                    sv.bpassign %18, %23 : i1
                    %25 = comb.concat %23, %22 : i1, i1
                    sv.bpassign %19, %25 : i2
                } else {
                    sv.bpassign %17, %7 : i1
                    sv.bpassign %18, %8 : i1
                    sv.bpassign %20, %23 : i1
                    sv.bpassign %21, %22 : i1
                    %26 = comb.concat %11, %10 : i1, i1
                    sv.bpassign %19, %26 : i2
                }
            }
        }
        %22 = comb.extract %I from 0 : (i2) -> i1
        %23 = comb.extract %I from 1 : (i2) -> i1
        %27 = comb.concat %16, %15 : i1, i1
        %28 = comb.concat %13, %12 : i1, i1
        %29 = comb.extract %28 from 0 : (i2) -> i1
        sv.verbatim "always @(*) WHEN_ASSERT_276: assert (~({{0}}) | ({{1}} == {{2}}));" (%0, %29, %3) : i1, i1, i1
        %30 = comb.extract %28 from 1 : (i2) -> i1
        sv.verbatim "always @(*) WHEN_ASSERT_277: assert (~({{0}}) | ({{1}} == {{2}}));" (%0, %30, %4) : i1, i1, i1
        %31 = comb.extract %I from 0 : (i2) -> i1
        %32 = comb.extract %14 from 0 : (i2) -> i1
        sv.verbatim "always @(*) WHEN_ASSERT_278: assert (~({{0}}) | ({{1}} == {{2}}));" (%0, %32, %31) : i1, i1, i1
        %33 = comb.extract %I from 1 : (i2) -> i1
        %34 = comb.extract %14 from 1 : (i2) -> i1
        sv.verbatim "always @(*) WHEN_ASSERT_279: assert (~({{0}}) | ({{1}} == {{2}}));" (%0, %34, %33) : i1, i1, i1
        %36 = hw.constant -1 : i1
        %35 = comb.xor %36, %0 : i1
        %37 = comb.and %35, %5 : i1
        sv.verbatim "always @(*) WHEN_ASSERT_280: assert (~({{0}}) | ({{1}} == {{2}}));" (%37, %29, %31) : i1, i1, i1
        sv.verbatim "always @(*) WHEN_ASSERT_281: assert (~({{0}}) | ({{1}} == {{2}}));" (%37, %30, %33) : i1, i1, i1
        sv.verbatim "always @(*) WHEN_ASSERT_282: assert (~({{0}}) | ({{1}} == {{2}}));" (%37, %32, %31) : i1, i1, i1
        sv.verbatim "always @(*) WHEN_ASSERT_283: assert (~({{0}}) | ({{1}} == {{2}}));" (%37, %34, %33) : i1, i1, i1
        %38 = comb.xor %36, %5 : i1
        %39 = comb.and %35, %38 : i1
        sv.verbatim "always @(*) WHEN_ASSERT_284: assert (~({{0}}) | ({{1}} == {{2}}));" (%39, %29, %7) : i1, i1, i1
        sv.verbatim "always @(*) WHEN_ASSERT_285: assert (~({{0}}) | ({{1}} == {{2}}));" (%39, %30, %8) : i1, i1, i1
        %40 = comb.extract %27 from 0 : (i2) -> i1
        sv.verbatim "always @(*) WHEN_ASSERT_286: assert (~({{0}}) | ({{1}} == {{2}}));" (%39, %40, %33) : i1, i1, i1
        %41 = comb.extract %27 from 1 : (i2) -> i1
        sv.verbatim "always @(*) WHEN_ASSERT_287: assert (~({{0}}) | ({{1}} == {{2}}));" (%39, %41, %31) : i1, i1, i1
        sv.verbatim "always @(*) WHEN_ASSERT_288: assert (~({{0}}) | ({{1}} == {{2}}));" (%39, %32, %10) : i1, i1, i1
        sv.verbatim "always @(*) WHEN_ASSERT_289: assert (~({{0}}) | ({{1}} == {{2}}));" (%39, %34, %11) : i1, i1, i1
        sv.verbatim "always @(*) WHEN_ASSERT_290: assert (~({{0}}) | ({{1}} == {{2}}));" (%39, %40, %31) : i1, i1, i1
        sv.verbatim "always @(*) WHEN_ASSERT_291: assert (~({{0}}) | ({{1}} == {{2}}));" (%39, %41, %33) : i1, i1, i1
        hw.output %27, %28, %14 : i2, i2, i2
    }
}
