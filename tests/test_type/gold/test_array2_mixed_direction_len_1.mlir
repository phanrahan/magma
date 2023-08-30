module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @test_array2_mixed_direction_len_1(%I_0_x: i1, %O_0_y: i1) -> (I_0_y: i1, O_0_x: i1) {
        hw.output %O_0_y, %I_0_x : i1, i1
    }
}
