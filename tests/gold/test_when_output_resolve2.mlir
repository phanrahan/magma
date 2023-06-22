module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_output_resolve2(%I: i8, %x: i1) -> (O0: i8, O1: i8) {
        %1 = hw.constant -1 : i8
        %0 = comb.xor %1, %I : i8
        %3 = sv.reg name "_WHEN_WIRE_102" : !hw.inout<i8>
        %2 = sv.read_inout %3 : !hw.inout<i8>
        sv.alwayscomb {
            sv.if %x {
                sv.bpassign %3, %I : i8
            } else {
                sv.bpassign %3, %0 : i8
            }
        }
        sv.verbatim "WHEN_ASSERT_197: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%x, %2, %I) : i1, i8, i8
        %5 = hw.constant -1 : i1
        %4 = comb.xor %5, %x : i1
        sv.verbatim "WHEN_ASSERT_198: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%4, %2, %0) : i1, i8, i8
        hw.output %2, %2 : i8, i8
    }
}
