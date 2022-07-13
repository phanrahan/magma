hw.module @test_when_override(%I: i2, %S: i1) -> (O: i1) {
    %0 = comb.extract %I from 1 : (i2) -> i1
    %1 = comb.extract %I from 0 : (i2) -> i1
    hw.output %0 : i1
}
