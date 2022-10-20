module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @simple_wire(%I: i8) -> (O: i8) {
        %1 = sv.wire sym @simple_wire.tmp {name="tmp"} : !hw.inout<i8>
        sv.assign %1, %I : i8
        %0 = sv.read_inout %1 : !hw.inout<i8>
        hw.output %0 : i8
    }
}
