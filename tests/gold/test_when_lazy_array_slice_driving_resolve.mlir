module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_lazy_array_slice_driving_resolve(%S: i1) -> (O: i4) {
        %0 = hw.constant 1 : i1
        %1 = hw.constant 2 : i4
        %2 = hw.constant 4 : i4
        %3 = hw.constant 0 : i1
        %4 = hw.constant 1 : i1
        %6 = sv.reg : !hw.inout<i4>
        %5 = sv.read_inout %6 : !hw.inout<i4>
        sv.alwayscomb {
            sv.if %S {
                %7 = comb.concat %3, %3, %4, %3 : i1, i1, i1, i1
                sv.bpassign %6, %7 : i4
            } else {
                %8 = comb.concat %3, %4, %3, %3 : i1, i1, i1, i1
                sv.bpassign %6, %8 : i4
            }
        }
        %9 = comb.extract %5 from 1 : (i4) -> i1
        %10 = comb.extract %5 from 2 : (i4) -> i1
        %11 = comb.extract %5 from 3 : (i4) -> i1
        %12 = comb.concat %11, %10, %9, %0 : i1, i1, i1, i1
        %14 = sv.wire sym @test_when_lazy_array_slice_driving_resolve.x name "x" : !hw.inout<i4>
        sv.assign %14, %12 : i4
        %13 = sv.read_inout %14 : !hw.inout<i4>
        %15 = comb.extract %13 from 0 : (i4) -> i1
        %16 = hw.constant 0 : i1
        sv.verbatim "always @(*) WHEN_ASSERT_120: assert (~({{0}}) | ({{1}} == {{2}}));" (%S, %15, %16) : i1, i1, i1
        %17 = comb.extract %13 from 1 : (i4) -> i1
        %18 = hw.constant 1 : i1
        sv.verbatim "always @(*) WHEN_ASSERT_121: assert (~({{0}}) | ({{1}} == {{2}}));" (%S, %17, %18) : i1, i1, i1
        %19 = comb.extract %13 from 2 : (i4) -> i1
        %20 = hw.constant 0 : i1
        sv.verbatim "always @(*) WHEN_ASSERT_122: assert (~({{0}}) | ({{1}} == {{2}}));" (%S, %19, %20) : i1, i1, i1
        %21 = comb.extract %13 from 3 : (i4) -> i1
        %22 = hw.constant 0 : i1
        sv.verbatim "always @(*) WHEN_ASSERT_123: assert (~({{0}}) | ({{1}} == {{2}}));" (%S, %21, %22) : i1, i1, i1
        %24 = hw.constant -1 : i1
        %23 = comb.xor %24, %S : i1
        %25 = hw.constant 0 : i1
        sv.verbatim "always @(*) WHEN_ASSERT_124: assert (~({{0}}) | ({{1}} == {{2}}));" (%23, %15, %25) : i1, i1, i1
        %26 = hw.constant 0 : i1
        sv.verbatim "always @(*) WHEN_ASSERT_125: assert (~({{0}}) | ({{1}} == {{2}}));" (%23, %17, %26) : i1, i1, i1
        %27 = hw.constant 1 : i1
        sv.verbatim "always @(*) WHEN_ASSERT_126: assert (~({{0}}) | ({{1}} == {{2}}));" (%23, %19, %27) : i1, i1, i1
        %28 = hw.constant 0 : i1
        sv.verbatim "always @(*) WHEN_ASSERT_127: assert (~({{0}}) | ({{1}} == {{2}}));" (%23, %21, %28) : i1, i1, i1
        hw.output %13 : i4
    }
}
