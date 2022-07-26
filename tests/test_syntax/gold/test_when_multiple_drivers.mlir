hw.module @test_when_multiple_drivers(%I: i2, %S: i2) -> (O0: i1, O1: i1) {
    %0 = comb.extract %I from 1 : (i2) -> i1
    %1 = comb.extract %S from 0 : (i2) -> i1
    %2 = comb.extract %S from 1 : (i2) -> i1
    %3 = comb.extract %I from 0 : (i2) -> i1
    %6 = sv.reg {name = "O0_reg"} : !hw.inout<i1>
    %7 = sv.reg {name = "O1_reg"} : !hw.inout<i1>
    sv.alwayscomb {
        sv.bpassign %6, %0 : i1
        sv.bpassign %7, %3 : i1
        sv.if %1 {
            sv.if %2 {
                sv.bpassign %6, %3 : i1
                sv.bpassign %7, %0 : i1
            }
        }
    }
    %4 = sv.read_inout %6 : !hw.inout<i1>
    %5 = sv.read_inout %7 : !hw.inout<i1>
    hw.output %4, %5 : i1, i1
}
