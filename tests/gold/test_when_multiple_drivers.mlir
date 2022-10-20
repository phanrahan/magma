module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_multiple_drivers(%I: i2, %S: i2) -> (O0: i1, O1: i1) {
        %0 = comb.extract %S from 0 : (i2) -> i1
        %1 = comb.extract %S from 1 : (i2) -> i1
        %2 = comb.extract %I from 1 : (i2) -> i1
        %3 = comb.extract %I from 0 : (i2) -> i1
        %6 = sv.reg : !hw.inout<i1>
        %4 = sv.read_inout %6 : !hw.inout<i1>
        %7 = sv.reg : !hw.inout<i1>
        %5 = sv.read_inout %7 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %6, %2 : i1
            sv.bpassign %7, %3 : i1
            sv.if %0 {
                sv.if %1 {
                    sv.bpassign %6, %3 : i1
                    sv.bpassign %7, %2 : i1
                }
            }
        }
        hw.output %4, %5 : i1, i1
    }
}
