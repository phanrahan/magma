hw.module @test_when_nested_Tuplex_Bits2_y_Bit(%I_0_x: i2, %I_0_y: i1, %I_1_x: i2, %I_1_y: i1, %S: i1) -> (O_x: i2, O_y: i1) {
    %1 = sv.reg : !hw.inout<i1>
    %0 = sv.read_inout %1 : !hw.inout<i1>
    sv.alwayscomb {
        sv.bpassign %1, %I_1_y : i1
        sv.if %S {
            sv.bpassign %1, %I_0_y : i1
        }
    }
    hw.output %I_0_x, %0 : i2, i1
}
