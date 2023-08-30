module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module.extern @Foo(%I: i8) -> (O: i8)
    hw.module @test_namer_dict_already_named(%I: i8) -> (O: i8) {
        %1 = sv.wire sym @test_namer_dict_already_named.y name "y" : !hw.inout<i8>
        sv.assign %1, %I : i8
        %0 = sv.read_inout %1 : !hw.inout<i8>
        %2 = hw.instance "bar" @Foo(I: %0: i8) -> (O: i8)
        hw.output %2 : i8
    }
}
