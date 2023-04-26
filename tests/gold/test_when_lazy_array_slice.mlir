module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_lazy_array_slice(%S: i1) -> (O: i4) {
        %0 = hw.constant 0 : i2
        %1 = hw.constant 1 : i2
        %2 = hw.constant 1 : i2
        %3 = hw.constant 0 : i2
        %4 = hw.constant 0 : i1
        %5 = hw.constant 1 : i1
        %12 = sv.reg : !hw.inout<i2>
        %6 = sv.read_inout %12 : !hw.inout<i2>
        %13 = sv.reg : !hw.inout<i2>
        %7 = sv.read_inout %13 : !hw.inout<i2>
        %14 = sv.reg : !hw.inout<i1>
        %8 = sv.read_inout %14 : !hw.inout<i1>
        %15 = sv.reg : !hw.inout<i1>
        %9 = sv.read_inout %15 : !hw.inout<i1>
        %16 = sv.reg : !hw.inout<i1>
        %10 = sv.read_inout %16 : !hw.inout<i1>
        %17 = sv.reg : !hw.inout<i1>
        %11 = sv.read_inout %17 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %S {
                sv.bpassign %14, %4 : i1
                sv.bpassign %15, %4 : i1
                sv.bpassign %16, %5 : i1
                sv.bpassign %17, %4 : i1
            } else {
                sv.bpassign %14, %5 : i1
                sv.bpassign %15, %4 : i1
                sv.bpassign %16, %4 : i1
                sv.bpassign %17, %4 : i1
            }
        }
        %18 = comb.concat %11, %10, %9, %8 : i1, i1, i1, i1
        %20 = sv.wire sym @test_when_lazy_array_slice.x name "x" : !hw.inout<i4>
        sv.assign %20, %18 : i4
        %19 = sv.read_inout %20 : !hw.inout<i4>
        %21 = comb.extract %19 from 0 : (i4) -> i1
        %22 = hw.constant 0 : i1
        sv.verbatim "always @(*) WHEN_ASSERT_100: assert (~({{0}}) | ({{1}} == {{2}}));" (%S, %21, %22) : i1, i1, i1
        %23 = comb.extract %19 from 1 : (i4) -> i1
        %24 = hw.constant 0 : i1
        sv.verbatim "always @(*) WHEN_ASSERT_101: assert (~({{0}}) | ({{1}} == {{2}}));" (%S, %23, %24) : i1, i1, i1
        %25 = comb.extract %19 from 2 : (i4) -> i1
        %26 = hw.constant 1 : i1
        sv.verbatim "always @(*) WHEN_ASSERT_102: assert (~({{0}}) | ({{1}} == {{2}}));" (%S, %25, %26) : i1, i1, i1
        %27 = comb.extract %19 from 3 : (i4) -> i1
        %28 = hw.constant 0 : i1
        sv.verbatim "always @(*) WHEN_ASSERT_103: assert (~({{0}}) | ({{1}} == {{2}}));" (%S, %27, %28) : i1, i1, i1
        %30 = hw.constant -1 : i1
        %29 = comb.xor %30, %S : i1
        %31 = hw.constant 1 : i1
        sv.verbatim "always @(*) WHEN_ASSERT_104: assert (~({{0}}) | ({{1}} == {{2}}));" (%29, %21, %31) : i1, i1, i1
        %32 = hw.constant 0 : i1
        sv.verbatim "always @(*) WHEN_ASSERT_105: assert (~({{0}}) | ({{1}} == {{2}}));" (%29, %23, %32) : i1, i1, i1
        %33 = hw.constant 0 : i1
        sv.verbatim "always @(*) WHEN_ASSERT_106: assert (~({{0}}) | ({{1}} == {{2}}));" (%29, %25, %33) : i1, i1, i1
        %34 = hw.constant 0 : i1
        sv.verbatim "always @(*) WHEN_ASSERT_107: assert (~({{0}}) | ({{1}} == {{2}}));" (%29, %27, %34) : i1, i1, i1
        hw.output %19 : i4
    }
}
