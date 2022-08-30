hw.module @test_when_nested_complex(%I: i2, %S: i2) -> (O: i1) {
    %0 = comb.extract %S from 1 : (i2) -> i1
    %2 = hw.constant -1 : i2
    %1 = comb.icmp eq %S, %2 : i2
    %3 = comb.extract %S from 0 : (i2) -> i1
    %4 = hw.constant 1 : i1
    %5 = comb.extract %I from 0 : (i2) -> i1
    %6 = comb.extract %I from 1 : (i2) -> i1
    %8 = sv.reg : !hw.inout<i1>
    %7 = sv.read_inout %8 : !hw.inout<i1>
    sv.alwayscomb {
        sv.bpassign %8, %4 : i1
        sv.if %3 {
            sv.bpassign %8, %5 : i1
            sv.if %0 {
                sv.bpassign %8, %6 : i1
            }
        }
    }
    %9 = hw.constant 1 : i1
    %11 = sv.reg : !hw.inout<i1>
    %10 = sv.read_inout %11 : !hw.inout<i1>
    sv.alwayscomb {
        sv.bpassign %11, %7 : i1
        sv.if %0 {
            sv.if %1 {
                sv.bpassign %11, %9 : i1
            } else {
                sv.bpassign %11, %9 : i1
            }
        }
    }
    hw.output %10 : i1
}
