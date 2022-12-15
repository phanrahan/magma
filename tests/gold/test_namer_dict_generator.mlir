module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @Foo(%I: i8) -> (O: i8) {
        %1 = sv.wire sym @Foo.x {name="x"} : !hw.inout<i8>
        sv.assign %1, %I : i8
        %0 = sv.read_inout %1 : !hw.inout<i8>
        hw.output %0 : i8
    }
}
