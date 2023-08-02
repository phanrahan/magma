module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_output_resolve2(%I: i8, %x: i1) -> (O0: i8, O1: i8) {
        %1 = hw.constant -1 : i8
        %0 = comb.xor %1, %I : i8
        %3 = sv.reg : !hw.inout<i8>
        %2 = sv.read_inout %3 : !hw.inout<i8>
        sv.alwayscomb {
            sv.if %x {
                sv.bpassign %3, %I : i8
            } else {
                sv.bpassign %3, %0 : i8
            }
        }
        %5 = sv.wire sym @test_when_output_resolve2._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i8>
        sv.assign %5, %2 : i8
        %4 = sv.read_inout %5 : !hw.inout<i8>
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%x, %4, %I) : i1, i8, i8
        %7 = hw.constant -1 : i1
        %6 = comb.xor %7, %x : i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%6, %4, %0) : i1, i8, i8
        hw.output %4, %4 : i8, i8
    }
}
