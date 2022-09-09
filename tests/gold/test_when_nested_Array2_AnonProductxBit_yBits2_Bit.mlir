hw.module @test_when_nested_Array2_AnonProductxBit_yBits2_Bit(%I_0_0_x: i1, %I_0_0_y: i2, %I_0_1_x: i1, %I_0_1_y: i2, %I_1_0_x: i1, %I_1_0_y: i2, %I_1_1_x: i1, %I_1_1_y: i2, %S: i1) -> (O_0_x: i1, O_0_y: i2, O_1_x: i1, O_1_y: i2) {
    sv.alwayscomb {
        sv.if %S {
        }
    }
    hw.output %I_0_0_x, %I_0_0_y, %I_0_1_x, %I_0_1_y : i1, i2, i1, i2
}
