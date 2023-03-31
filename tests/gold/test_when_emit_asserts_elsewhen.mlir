module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_emit_asserts_elsewhen(%I: i2, %S: i2) -> (O: i1) {
        %0 = comb.extract %S from 0 : (i2) -> i1
        %1 = comb.extract %I from 1 : (i2) -> i1
        %2 = comb.extract %I from 0 : (i2) -> i1
        %3 = comb.extract %S from 1 : (i2) -> i1
        %5 = hw.constant -1 : i1
        %4 = comb.xor %5, %2 : i1
        %9 = sv.reg : !hw.inout<i1>
        %6 = sv.read_inout %9 : !hw.inout<i1>
        %10 = sv.reg : !hw.inout<i1>
        %7 = sv.read_inout %10 : !hw.inout<i1>
        %11 = sv.reg : !hw.inout<i1>
        %8 = sv.read_inout %11 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %11, %1 : i1
            sv.if %0 {
                sv.bpassign %11, %2 : i1
            } else {
                sv.if %3 {
                    sv.bpassign %11, %4 : i1
                }
            }
        }
        sv.verbatim "always @(*) assert (~({{0}}) | ({{1}} == {{2}}));" (%0, %8, %2) : i1, i1, i1
        %12 = comb.xor %5, %0 : i1
        %13 = comb.and %12, %3 : i1
        sv.verbatim "always @(*) assert (~({{0}}) | ({{1}} == {{2}}));" (%13, %8, %4) : i1, i1, i1
        hw.output %8 : i1
    }
}
