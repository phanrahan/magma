module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @test_array2_mixed_direction_len_1(in %I_0_x: i1, in %O_0_y: i1, out I_0_y: i1, out O_0_x: i1) {
        hw.output %O_0_y, %I_0_x : i1, i1
    }
}
