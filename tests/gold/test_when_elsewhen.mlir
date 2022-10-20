module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_elsewhen(%I: i3, %S: i2) -> (O: i1) {
        %0 = comb.extract %S from 0 : (i2) -> i1
        %1 = comb.extract %I from 0 : (i3) -> i1
        %2 = comb.extract %S from 1 : (i2) -> i1
        %3 = comb.extract %I from 1 : (i3) -> i1
        %4 = comb.extract %I from 2 : (i3) -> i1
        %6 = sv.reg : !hw.inout<i1>
        %5 = sv.read_inout %6 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %0 {
                sv.bpassign %6, %1 : i1
            } else {
                sv.if %2 {
                    sv.bpassign %6, %3 : i1
                } else {
                    sv.bpassign %6, %4 : i1
                }
            }
        }
        hw.output %5 : i1
    }
}
