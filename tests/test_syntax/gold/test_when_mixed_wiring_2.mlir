hw.module @test_when_mixed_wiring_2(%I: i2, %S: i2) -> (O: i1) {
    %0 = comb.extract %S from 0 : (i2) -> i1
    %1 = comb.extract %S from 1 : (i2) -> i1
    %2 = comb.extract %I from 0 : (i2) -> i1
    %3 = hw.constant 1 : i1
    %4 = comb.and %2, %3 : i1
    %5 = comb.extract %I from 1 : (i2) -> i1
    %6 = hw.constant 1 : i1
    %7 = comb.xor %5, %6 : i1
    %8 = hw.constant 1 : i1
    %11 = sv.reg {name = "AnonymousValue_140525425816288_reg"} : !hw.inout<i1>
    %12 = sv.reg {name = "O_reg"} : !hw.inout<i1>
    sv.alwayscomb {
        sv.if %1 {
            sv.bpassign %11, %4 : i1
        } else {
            sv.bpassign %11, %7 : i1
        }
        sv.if %0 {
            sv.bpassign %12, %9 : i1
            sv.if %1 {
            } else {
            }
        } else {
            sv.bpassign %12, %8 : i1
        }
    }
    %9 = sv.read_inout %11 : !hw.inout<i1>
    %10 = sv.read_inout %12 : !hw.inout<i1>
    hw.output %10 : i1
}
