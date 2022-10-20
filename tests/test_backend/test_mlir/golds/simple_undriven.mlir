module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @simple_undriven() -> (O: i1) {
        %1 = sv.wire sym @simple_undriven.corebit_undriven_inst0 : !hw.inout<i1>
        %0 = sv.read_inout %1 : !hw.inout<i1>
        hw.output %0 : i1
    }
}
