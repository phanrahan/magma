hw.module @TopBasicAsserts_mlir(%I: i1, %O: i1, %other: i1) -> () {
}
hw.module @Top(%I: i1) -> (O: i1) {
    %1 = sv.wire sym @Top._magma_bind_wire_0 {name="_magma_bind_wire_0"} : !hw.inout<i1>
    sv.assign %1, %I : i1
    %0 = sv.read_inout %1 : !hw.inout<i1>
    hw.instance "TopBasicAsserts_mlir_inst" sym @Top.TopBasicAsserts_mlir_inst @TopBasicAsserts_mlir(I: %I: i1, O: %I: i1, other: %I: i1) -> () {doNotPrint = 1}
    hw.output %I : i1
}
sv.bind #hw.innerNameRef<@Top::@Top.TopBasicAsserts_mlir_inst>
