module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @simple_wrap_cast(%I: i1) -> (O: i1) {
        %1 = sv.wire sym @simple_wrap_cast.coreir_wrapInClock_inst0 {name="coreir_wrapInClock_inst0"} : !hw.inout<i1>
        sv.assign %1, %I : i1
        %0 = sv.read_inout %1 : !hw.inout<i1>
        hw.output %0 : i1
    }
}
