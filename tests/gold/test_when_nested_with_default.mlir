module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_nested_with_default(%I: i2, %S: i2) -> (O: i1) {
        %0 = comb.extract %S from 0 : (i2) -> i1
        %1 = comb.extract %S from 1 : (i2) -> i1
        %2 = comb.extract %I from 1 : (i2) -> i1
        %3 = comb.extract %I from 0 : (i2) -> i1
        %5 = sv.reg : !hw.inout<i1>
        %4 = sv.read_inout %5 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %5, %2 : i1
            sv.if %0 {
                sv.if %1 {
                    sv.bpassign %5, %3 : i1
                }
            }
        }
        hw.output %4 : i1
    }
}
