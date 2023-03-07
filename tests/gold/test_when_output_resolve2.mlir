module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_output_resolve2(%I: i8, %x: i1) -> (O0: i8, O1: i8) {
        %1 = hw.constant -1 : i8
        %0 = comb.xor %1, %I : i8
        %4 = sv.reg : !hw.inout<i8>
        %2 = sv.read_inout %4 : !hw.inout<i8>
        %5 = sv.reg : !hw.inout<i8>
        %3 = sv.read_inout %5 : !hw.inout<i8>
        sv.alwayscomb {
            sv.if %x {
                sv.bpassign %4, %I : i8
                sv.bpassign %5, %I : i8
            } else {
                sv.bpassign %4, %0 : i8
                sv.bpassign %5, %0 : i8
            }
        }
        hw.output %2, %3 : i8, i8
    }
}
