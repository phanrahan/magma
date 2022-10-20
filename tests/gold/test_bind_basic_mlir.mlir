module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @Top(%I: i1) -> (O: i1) {
        %1 = sv.wire sym @Top._magma_bind_wire_0 {name="_magma_bind_wire_0"} : !hw.inout<i1>
        sv.assign %1, %I : i1
        %0 = sv.read_inout %1 : !hw.inout<i1>
        hw.output %I : i1
    }
}
