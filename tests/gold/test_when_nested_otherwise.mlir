module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_nested_otherwise(%I: i2, %S: i2) -> (O: i2) {
        %1 = hw.constant -1 : i2
        %0 = comb.icmp eq %S, %1 : i2
        %2 = comb.extract %S from 1 : (i2) -> i1
        %4 = hw.constant -1 : i2
        %3 = comb.xor %4, %I : i2
        %6 = sv.reg : !hw.inout<i2>
        %5 = sv.read_inout %6 : !hw.inout<i2>
        sv.alwayscomb {
            sv.if %0 {
                sv.bpassign %6, %I : i2
            } else {
                sv.if %2 {
                    sv.bpassign %6, %3 : i2
                } else {
                    sv.bpassign %6, %I : i2
                }
            }
        }
        hw.output %5 : i2
    }
}
