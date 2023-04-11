module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_emit_asserts_nesting(%I: i2, %S: i2) -> (O: i1) {
        %0 = comb.extract %S from 0 : (i2) -> i1
        %1 = comb.extract %S from 1 : (i2) -> i1
        %2 = comb.extract %I from 1 : (i2) -> i1
        %3 = comb.extract %I from 0 : (i2) -> i1
        %5 = hw.constant -1 : i2
        %4 = comb.icmp eq %S, %5 : i2
        %7 = hw.constant -1 : i1
        %6 = comb.xor %7, %3 : i1
        %11 = sv.reg : !hw.inout<i1>
        %8 = sv.read_inout %11 : !hw.inout<i1>
        %12 = sv.reg : !hw.inout<i1>
        %9 = sv.read_inout %12 : !hw.inout<i1>
        %13 = sv.reg : !hw.inout<i1>
        %10 = sv.read_inout %13 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %13, %2 : i1
            sv.if %0 {
                sv.if %1 {
                    sv.bpassign %13, %3 : i1
                } else {
                    sv.if %4 {
                        sv.bpassign %13, %6 : i1
                    }
                }
            }
        }
        %14 = comb.and %0, %1 : i1
        sv.verbatim "always @(*) assert (~({{0}}) | ({{1}} == {{2}}));" (%14, %10, %3) : i1, i1, i1
        %15 = comb.xor %7, %1 : i1
        %16 = comb.and %0, %15 : i1
        %17 = comb.and %16, %4 : i1
        sv.verbatim "always @(*) assert (~({{0}}) | ({{1}} == {{2}}));" (%17, %10, %6) : i1, i1, i1
        hw.output %10 : i1
    }
}
