hw.module @Bottom(%I: i1) -> (O: i1) {
    hw.output %I : i1
}
hw.module @Middle(%I: i1) -> (O: i1) {
    %0 = hw.instance "bottom" @Bottom(I: %I: i1) -> (O: i1)
    hw.output %0 : i1
}
hw.module @TopXMRAsserts_mlir(%I: i1, %O: i1, %other: i1) -> () {
}
hw.module @Top(%I: i1) -> (O: i1) {
    %0 = hw.instance "middle" @Middle(I: %I: i1) -> (O: i1)
    %2 = sv.xmr "middle", "bottom", "I" : !hw.inout<i1>
    %1 = sv.read_inout %2 : !hw.inout<i1>
    hw.instance "TopXMRAsserts_mlir_inst0" sym @TopXMRAsserts_mlir_inst0 @TopXMRAsserts_mlir(I: %I: i1, O: %0: i1, other: %1: i1) -> () {doNotPrint = 1}
    hw.output %0 : i1
}
sv.bind #hw.innerNameRef<@Top::@TopXMRAsserts_mlir_inst0>
