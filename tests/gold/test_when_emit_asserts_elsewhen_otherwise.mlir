module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_emit_asserts_elsewhen_otherwise(%I: i2, %S: i2) -> (O: i1) {
        %0 = comb.extract %S from 0 : (i2) -> i1
        %1 = comb.extract %I from 0 : (i2) -> i1
        %2 = comb.extract %S from 1 : (i2) -> i1
        %4 = hw.constant -1 : i1
        %3 = comb.xor %4, %1 : i1
        %5 = comb.extract %I from 1 : (i2) -> i1
        %10 = sv.reg : !hw.inout<i1>
        %6 = sv.read_inout %10 : !hw.inout<i1>
        %11 = sv.reg : !hw.inout<i1>
        %7 = sv.read_inout %11 : !hw.inout<i1>
        %12 = sv.reg : !hw.inout<i1>
        %8 = sv.read_inout %12 : !hw.inout<i1>
        %13 = sv.reg : !hw.inout<i1>
        %9 = sv.read_inout %13 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %0 {
                sv.bpassign %13, %1 : i1
            } else {
                sv.if %2 {
                    sv.bpassign %13, %3 : i1
                } else {
                    sv.bpassign %13, %5 : i1
                }
            }
        }
        sv.verbatim "always @(*) assert (~({{0}}) | ({{1}} == {{2}}));" (%0, %9, %1) : i1, i1, i1
        %14 = comb.xor %4, %0 : i1
        %15 = comb.and %14, %2 : i1
        sv.verbatim "always @(*) assert (~({{0}}) | ({{1}} == {{2}}));" (%15, %9, %3) : i1, i1, i1
        %16 = comb.xor %4, %2 : i1
        %17 = comb.and %14, %16 : i1
        sv.verbatim "always @(*) assert (~({{0}}) | ({{1}} == {{2}}));" (%17, %9, %5) : i1, i1, i1
        hw.output %9 : i1
    }
}