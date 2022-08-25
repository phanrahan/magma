hw.module @test_mlir_primitive_neg(%I: i2) -> (O: i2) {
    %1 = hw.constant 0 : i2
    %0 = comb.sub %1, %I : i2
    hw.output %0 : i2
}
