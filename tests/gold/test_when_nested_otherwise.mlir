hw.module @test_when_nested_otherwise(%I: i2, %S: i2) -> (O: i2) {
    %1 = hw.constant -1 : i2
    %0 = comb.icmp eq %S, %1 : i2
    %2 = comb.extract %I from 0 : (i2) -> i1
    %3 = comb.extract %I from 1 : (i2) -> i1
    %4 = comb.extract %S from 1 : (i2) -> i1
    %6 = hw.constant -1 : i2
    %5 = comb.xor %6, %I : i2
    %7 = comb.extract %5 from 0 : (i2) -> i1
    %8 = comb.extract %5 from 1 : (i2) -> i1
    %11 = sv.reg : !hw.inout<i1>
    %9 = sv.read_inout %11 : !hw.inout<i1>
    %12 = sv.reg : !hw.inout<i1>
    %10 = sv.read_inout %12 : !hw.inout<i1>
    sv.alwayscomb {
        sv.if %0 {
            sv.bpassign %11, %2 : i1
            sv.bpassign %12, %3 : i1
        } else {
            sv.if %4 {
                sv.bpassign %11, %7 : i1
                sv.bpassign %12, %8 : i1
            } else {
                sv.bpassign %11, %2 : i1
                sv.bpassign %12, %3 : i1
            }
        }
    }
    %13 = comb.concat %10, %9 : i1, i1
    hw.output %13 : i2
}
