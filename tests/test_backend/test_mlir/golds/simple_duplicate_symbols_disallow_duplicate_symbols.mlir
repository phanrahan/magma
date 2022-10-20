module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @simple_duplicate_symbols(%I: i1) -> (O: i2) {
        %1 = sv.wire sym @simple_duplicate_symbols.x {name="x"} : !hw.inout<i1>
        sv.assign %1, %I : i1
        %0 = sv.read_inout %1 : !hw.inout<i1>
        %3 = sv.wire sym @simple_duplicate_symbols.x {name="x"} : !hw.inout<i1>
        sv.assign %3, %I : i1
        %2 = sv.read_inout %3 : !hw.inout<i1>
        %4 = comb.concat %2, %0 : i1, i1
        hw.output %4 : i2
    }
}
