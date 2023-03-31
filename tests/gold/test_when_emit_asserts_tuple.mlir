module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_emit_asserts_tuple(%I_0_0: i8, %I_0_1: i1, %I_1_0: i8, %I_1_1: i1, %S: i1) -> (O_0: i8, O_1: i1) {
        %4 = sv.reg : !hw.inout<i8>
        %0 = sv.read_inout %4 : !hw.inout<i8>
        %5 = sv.reg : !hw.inout<i1>
        %1 = sv.read_inout %5 : !hw.inout<i1>
        %6 = sv.reg : !hw.inout<i8>
        %2 = sv.read_inout %6 : !hw.inout<i8>
        %7 = sv.reg : !hw.inout<i1>
        %3 = sv.read_inout %7 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %6, %I_1_0 : i8
            sv.bpassign %7, %I_1_1 : i1
            sv.if %S {
                sv.bpassign %6, %I_0_0 : i8
                sv.bpassign %7, %I_0_1 : i1
            }
        }
        sv.verbatim "always @(*) assert (~({{0}}) | ({{1}} == {{2}}));" (%S, %2, %I_0_0) : i1, i8, i8
        sv.verbatim "always @(*) assert (~({{0}}) | ({{1}} == {{2}}));" (%S, %3, %I_0_1) : i1, i1, i1
        hw.output %2, %3 : i8, i1
    }
}
