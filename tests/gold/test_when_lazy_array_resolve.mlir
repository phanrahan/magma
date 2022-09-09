hw.module @test_when_lazy_array_resolve(%I: i2, %S: i1) -> (O: i2) {
    %0 = comb.extract %I from 0 : (i2) -> i1
    %1 = comb.extract %I from 1 : (i2) -> i1
    %2 = hw.constant 1 : i2
    %3 = comb.shru %I, %2 : i2
    %4 = comb.extract %3 from 0 : (i2) -> i1
    %5 = comb.extract %3 from 1 : (i2) -> i1
    %8 = sv.reg : !hw.inout<i1>
    %6 = sv.read_inout %8 : !hw.inout<i1>
    %9 = sv.reg : !hw.inout<i1>
    %7 = sv.read_inout %9 : !hw.inout<i1>
    sv.alwayscomb {
        sv.if %S {
            sv.bpassign %8, %0 : i1
            sv.bpassign %9, %1 : i1
        } else {
            sv.bpassign %8, %4 : i1
            sv.bpassign %9, %5 : i1
        }
    }
    %10 = comb.concat %7, %6 : i1, i1
    hw.output %10 : i2
}
