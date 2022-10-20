module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @Bottom(%I: i1) -> (O: i1) {
        hw.output %I : i1
    }
    hw.module @Middle(%I: i1) -> (O: i1) {
        %0 = hw.instance "bottom" @Bottom(I: %I: i1) -> (O: i1)
        %2 = sv.wire sym @Middle._magma_bind_wire_0 {name="_magma_bind_wire_0"} : !hw.inout<i1>
        sv.assign %2, %I : i1
        %1 = sv.read_inout %2 : !hw.inout<i1>
        hw.output %0 : i1
    }
    hw.module @Top(%I: i1) -> (O: i1) {
        %0 = hw.instance "middle" @Middle(I: %I: i1) -> (O: i1)
        hw.output %0 : i1
    }
}
