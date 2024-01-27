module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @test_namer_dict_explicit_collision_value(in %I: i8, out O: i8) {
        %1 = sv.wire sym @test_namer_dict_explicit_collision_value.y_0 name "y_0" : !hw.inout<i8>
        sv.assign %1, %I : i8
        %0 = sv.read_inout %1 : !hw.inout<i8>
        %3 = sv.wire sym @test_namer_dict_explicit_collision_value.y_1 name "y_1" : !hw.inout<i8>
        sv.assign %3, %0 : i8
        %2 = sv.read_inout %3 : !hw.inout<i8>
        hw.output %2 : i8
    }
}
