module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_lazy_array_resolve(%I: i2, %S: i1) -> (O: i2) {
        %0 = comb.extract %I from 0 : (i2) -> i1
        %1 = comb.extract %I from 1 : (i2) -> i1
        %2 = hw.constant 1 : i2
        %3 = comb.shru %I, %2 : i2
        %4 = comb.extract %3 from 0 : (i2) -> i1
        %5 = comb.extract %3 from 1 : (i2) -> i1
        %9 = sv.reg : !hw.inout<i2>
        %6 = sv.read_inout %9 : !hw.inout<i2>
        %10 = sv.reg : !hw.inout<i1>
        %7 = sv.read_inout %10 : !hw.inout<i1>
        %11 = sv.reg : !hw.inout<i1>
        %8 = sv.read_inout %11 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %S {
                sv.bpassign %10, %0 : i1
                sv.bpassign %11, %1 : i1
            } else {
                sv.bpassign %10, %4 : i1
                sv.bpassign %11, %5 : i1
            }
        }
        %12 = comb.concat %8, %7 : i1, i1
        hw.output %12 : i2
    }
}
