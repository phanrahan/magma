module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @test_recursive_non_port(%I: i2, %S: i1) -> (O0: i1, O1: i1) {
        %0 = comb.extract %I from 0 : (i2) -> i1
        %1 = comb.extract %I from 1 : (i2) -> i1
        %3 = sv.reg : !hw.inout<i1>
        %2 = sv.read_inout %3 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %S {
                sv.bpassign %3, %0 : i1
            } else {
                sv.bpassign %3, %1 : i1
            }
        }
        %6 = sv.reg : !hw.inout<i1>
        %4 = sv.read_inout %6 : !hw.inout<i1>
        %7 = sv.reg : !hw.inout<i1>
        %5 = sv.read_inout %7 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %S {
                sv.bpassign %7, %2 : i1
            } else {
                sv.bpassign %7, %2 : i1
            }
        }
        hw.output %2, %5 : i1, i1
    }
}
