module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_recursive_non_port(%I: i2, %S: i1) -> (O0: i1, O1: i1) {
        %0 = comb.extract %I from 0 : (i2) -> i1
        %1 = comb.extract %I from 1 : (i2) -> i1
        %4 = sv.reg : !hw.inout<i1>
        %2 = sv.read_inout %4 : !hw.inout<i1>
        %5 = sv.reg : !hw.inout<i1>
        %3 = sv.read_inout %5 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %S {
                sv.bpassign %4, %0 : i1
                sv.bpassign %5, %2 : i1
            } else {
                sv.bpassign %4, %1 : i1
                sv.bpassign %5, %2 : i1
            }
        }
        hw.output %2, %3 : i1, i1
    }
}
