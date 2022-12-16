module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @Foo(%I: i4) -> (O: i1) {
        %1 = hw.constant -1 : i4
        %0 = comb.xor %1, %I : i4
        %3 = sv.wire sym @Foo.x {name="x"} : !hw.inout<i4>
        sv.assign %3, %0 : i4
        %2 = sv.read_inout %3 : !hw.inout<i4>
        %4 = comb.parity %2 : i4
        hw.output %4 : i1
    }
}
