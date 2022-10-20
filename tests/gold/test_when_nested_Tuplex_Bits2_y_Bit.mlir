module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_nested_Tuplex_Bits2_y_Bit(%I_0_x: i2, %I_0_y: i1, %I_1_x: i2, %I_1_y: i1, %S: i1) -> (O_x: i2, O_y: i1) {
        %2 = sv.reg : !hw.inout<i2>
        %0 = sv.read_inout %2 : !hw.inout<i2>
        %3 = sv.reg : !hw.inout<i1>
        %1 = sv.read_inout %3 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %2, %I_1_x : i2
            sv.bpassign %3, %I_1_y : i1
            sv.if %S {
                sv.bpassign %2, %I_0_x : i2
                sv.bpassign %3, %I_0_y : i1
            }
        }
        hw.output %0, %1 : i2, i1
    }
}
