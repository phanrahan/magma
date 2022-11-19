module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_non_port(%I: i2, %S: i1) -> (O: i1) {
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
        %5 = sv.wire sym @test_non_port.x {name="x"} : !hw.inout<i1>
        sv.assign %5, %2 : i1
        %4 = sv.read_inout %5 : !hw.inout<i1>
        hw.output %4 : i1
    }
}
