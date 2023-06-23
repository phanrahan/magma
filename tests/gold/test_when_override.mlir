module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_override(%I: i2, %S: i1) -> (O: i1) {
        %0 = comb.extract %I from 1 : (i2) -> i1
        %1 = comb.extract %I from 0 : (i2) -> i1
        %3 = hw.constant -1 : i1
        %2 = comb.xor %3, %S : i1
        %5 = sv.reg name "_WHEN_WIRE_0" : !hw.inout<i1>
        %4 = sv.read_inout %5 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %5, %0 : i1
            sv.if %S {
                sv.bpassign %5, %1 : i1
            }
        }
        hw.output %0 : i1
    }
}
