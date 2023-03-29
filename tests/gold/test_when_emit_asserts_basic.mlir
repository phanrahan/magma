module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_emit_asserts_basic(%I: i2, %S: i1) -> (O: i1) {
        %0 = comb.extract %I from 0 : (i2) -> i1
        %2 = sv.reg : !hw.inout<i1>
        %1 = sv.read_inout %2 : !hw.inout<i1>
        sv.verbatim "always @(*) assert (~{{0}} | ({{1}} == {{2}}));" (%S, %1, %0) : i1, i1, i1
        %3 = comb.extract %I from 1 : (i2) -> i1
        %5 = sv.reg : !hw.inout<i1>
        %4 = sv.read_inout %5 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %5, %3 : i1
            sv.if %S {
                sv.bpassign %5, %0 : i1
            }
        }
        hw.output %1 : i1
    }
}
