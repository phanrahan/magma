module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_double_elsewhen(%I: i2, %S: i2) -> (O: i1) {
        %0 = comb.extract %S from 0 : (i2) -> i1
        %1 = comb.extract %I from 0 : (i2) -> i1
        %2 = comb.extract %S from 1 : (i2) -> i1
        %3 = comb.extract %I from 1 : (i2) -> i1
        %5 = hw.constant -1 : i2
        %4 = comb.icmp eq %S, %5 : i2
        %6 = hw.constant 1 : i1
        %8 = sv.reg : !hw.inout<i1>
        %7 = sv.read_inout %8 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %0 {
                sv.bpassign %8, %1 : i1
            } else {
                sv.if %2 {
                    sv.bpassign %8, %3 : i1
                } else {
                    sv.if %4 {
                        sv.bpassign %8, %6 : i1
                    } else {
                        sv.bpassign %8, %6 : i1
                    }
                }
            }
        }
        hw.output %7 : i1
    }
}
