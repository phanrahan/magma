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
        hw.output %2, %2 : i8, i8
    }
}
