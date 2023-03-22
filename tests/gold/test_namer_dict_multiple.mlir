module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module.extern @Foo(%I: i8) -> (O: i8)
    hw.module @test_namer_dict_multiple(%I: i8) -> (O: i8) {
        %1 = sv.wire sym @test_namer_dict_multiple.x_0 name "x_0" : !hw.inout<i8>
        sv.assign %1, %I : i8
        %0 = sv.read_inout %1 : !hw.inout<i8>
        %2 = hw.instance "foo_0" @Foo(I: %0: i8) -> (O: i8)
        %4 = sv.wire sym @test_namer_dict_multiple.x_1 name "x_1" : !hw.inout<i8>
        sv.assign %4, %2 : i8
        %3 = sv.read_inout %4 : !hw.inout<i8>
        %5 = hw.instance "foo_1" @Foo(I: %3: i8) -> (O: i8)
        hw.output %5 : i8
    }
}
