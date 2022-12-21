module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module.extern @Foo(%I: i8) -> (O: i8)
    hw.module @test_namer_dict_explicit_collision_inst(%I: i8) -> (O: i8) {
        %0 = hw.instance "foo_0" @Foo(I: %I: i8) -> (O: i8)
        %1 = hw.instance "foo_1" @Foo(I: %0: i8) -> (O: i8)
        hw.output %1 : i8
    }
}
