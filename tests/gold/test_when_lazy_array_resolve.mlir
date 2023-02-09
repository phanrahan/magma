module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_lazy_array_resolve(%I: i2, %S: i1) -> (O: i2) {
        %0 = comb.extract %I from 0 : (i2) -> i1
        %1 = comb.extract %I from 1 : (i2) -> i1
        %2 = hw.constant 1 : i2
        %3 = comb.shru %I, %2 : i2
        %4 = comb.extract %3 from 0 : (i2) -> i1
        %5 = comb.extract %3 from 1 : (i2) -> i1
        %7 = sv.reg : !hw.inout<i2>
        %6 = sv.read_inout %7 : !hw.inout<i2>
        sv.alwayscomb {
            sv.if %S {
                %8 = comb.concat %1, %0 : i1, i1
                sv.bpassign %7, %8 : i2
            } else {
                %9 = comb.concat %5, %4 : i1, i1
                sv.bpassign %7, %9 : i2
            }
        }
        hw.output %6 : i2
    }
}
