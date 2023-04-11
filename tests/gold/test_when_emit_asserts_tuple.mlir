module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_emit_asserts_tuple(%I_0_0: i8, %I_0_1: i1, %I_1_0: i8, %I_1_1: i1, %S: i1) -> (O_0: i8, O_1: i1) {
        %6 = sv.reg : !hw.inout<i8>
        %0 = sv.read_inout %6 : !hw.inout<i8>
        %7 = sv.reg : !hw.inout<i1>
        %1 = sv.read_inout %7 : !hw.inout<i1>
        %8 = sv.reg : !hw.inout<i8>
        %2 = sv.read_inout %8 : !hw.inout<i8>
        %9 = sv.reg : !hw.inout<i1>
        %3 = sv.read_inout %9 : !hw.inout<i1>
        %10 = sv.reg : !hw.inout<i8>
        %4 = sv.read_inout %10 : !hw.inout<i8>
        %11 = sv.reg : !hw.inout<i1>
        %5 = sv.read_inout %11 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %10, %I_1_0 : i8
            sv.bpassign %11, %I_1_1 : i1
            sv.if %S {
                sv.bpassign %10, %I_0_0 : i8
                sv.bpassign %11, %I_0_1 : i1
            }
        }
        sv.verbatim "always @(*) assert (~({{0}}) | ({{1}} == {{2}}));" (%S, %4, %I_0_0) : i1, i8, i8
        sv.verbatim "always @(*) assert (~({{0}}) | ({{1}} == {{2}}));" (%S, %5, %I_0_1) : i1, i1, i1
        %13 = hw.constant -1 : i1
        %12 = comb.xor %13, %S : i1
        sv.verbatim "always @(*) assert (~({{0}}) | ({{1}} == {{2}}));" (%12, %4, %I_1_0) : i1, i8, i8
        sv.verbatim "always @(*) assert (~({{0}}) | ({{1}} == {{2}}));" (%12, %5, %I_1_1) : i1, i1, i1
        hw.output %4, %5 : i8, i1
    }
}
