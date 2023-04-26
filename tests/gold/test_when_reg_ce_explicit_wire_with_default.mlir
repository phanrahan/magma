module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_reg_ce_explicit_wire_with_default(%I: i8, %x: i1, %y: i1, %CLK: i1) -> (O: i8) {
        %0 = hw.constant 1 : i1
        %4 = sv.reg : !hw.inout<i8>
        %2 = sv.read_inout %4 : !hw.inout<i8>
        %5 = sv.reg : !hw.inout<i1>
        %3 = sv.read_inout %5 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %5, %0 : i1
            sv.bpassign %4, %1 : i8
            sv.if %y {
                sv.bpassign %4, %I : i8
                sv.bpassign %5, %x : i1
            }
        }
        %6 = sv.reg name "Register_inst0" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.if %3 {
                sv.passign %6, %2 : i8
            }
        }
        %7 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %6, %7 : i8
        }
        %1 = sv.read_inout %6 : !hw.inout<i8>
        sv.verbatim "always @(*) WHEN_ASSERT_174: assert (~({{0}}) | ({{1}} == {{2}}));" (%y, %2, %I) : i1, i8, i8
        sv.verbatim "always @(*) WHEN_ASSERT_175: assert (~({{0}}) | ({{1}} == {{2}}));" (%y, %3, %x) : i1, i1, i1
        %9 = hw.constant -1 : i1
        %8 = comb.xor %9, %y : i1
        %10 = hw.constant 1 : i1
        sv.verbatim "always @(*) WHEN_ASSERT_176: assert (~({{0}}) | ({{1}} == {{2}}));" (%8, %3, %10) : i1, i1, i1
        sv.verbatim "always @(*) WHEN_ASSERT_177: assert (~({{0}}) | ({{1}} == {{2}}));" (%8, %2, %1) : i1, i8, i8
        hw.output %1 : i8
    }
}
