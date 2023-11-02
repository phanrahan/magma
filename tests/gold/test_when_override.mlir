module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @test_when_override(in %I: i2, in %S: i1, out O: i1) {
        %0 = comb.extract %I from 1 : (i2) -> i1
        %1 = comb.extract %I from 0 : (i2) -> i1
        %3 = sv.reg : !hw.inout<i1>
        %2 = sv.read_inout %3 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %3, %0 : i1
            sv.if %S {
                sv.bpassign %3, %1 : i1
            }
        }
        hw.output %0 : i1
    }
}
