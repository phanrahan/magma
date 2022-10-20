module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @complex_undriven() -> (O: !hw.struct<x: i8, y: i1>) {
        %1 = sv.wire sym @complex_undriven.undriven_inst0 : !hw.inout<i8>
        %0 = sv.read_inout %1 : !hw.inout<i8>
        %3 = sv.wire sym @complex_undriven.corebit_undriven_inst0 : !hw.inout<i1>
        %2 = sv.read_inout %3 : !hw.inout<i1>
        %4 = hw.struct_create (%0, %2) : !hw.struct<x: i8, y: i1>
        hw.output %4 : !hw.struct<x: i8, y: i1>
    }
}
