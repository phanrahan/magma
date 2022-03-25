hw.module @Bottom(%I: !hw.struct<x: i1, y: i1>) -> (O: !hw.struct<x: i1, y: i1>) {
    hw.output %I : !hw.struct<x: i1, y: i1>
}
hw.module @Middle(%I: !hw.struct<x: i1, y: i1>) -> (O: !hw.struct<x: i1, y: i1>) {
    %0 = hw.instance "bottom" @Bottom(I: %I: !hw.struct<x: i1, y: i1>) -> (O: !hw.struct<x: i1, y: i1>)
    %2 = sv.wire sym @Middle.bind_value_0 {name="bind_value_0"} : !hw.inout<!hw.struct<x: i1, y: i1>>
    sv.assign %2, %0 : !hw.struct<x: i1, y: i1>
    %1 = sv.read_inout %2 : !hw.inout<!hw.struct<x: i1, y: i1>>
    %3 = hw.struct_extract %I["x"] : !hw.struct<x: i1, y: i1>
    %5 = sv.wire sym @Middle.bind_value_1 {name="bind_value_1"} : !hw.inout<i1>
    sv.assign %5, %3 : i1
    %4 = sv.read_inout %5 : !hw.inout<i1>
    hw.output %0 : !hw.struct<x: i1, y: i1>
}
hw.module @TopXMRAsserts_mlir(%I: !hw.struct<x: i1, y: i1>, %O: !hw.struct<x: i1, y: i1>, %a: !hw.struct<x: i1, y: i1>, %b: i1) -> () {
    %0 = hw.struct_extract %I["x"] : !hw.struct<x: i1, y: i1>
    %1 = hw.struct_extract %I["y"] : !hw.struct<x: i1, y: i1>
    %2 = hw.struct_extract %O["x"] : !hw.struct<x: i1, y: i1>
    %3 = hw.struct_extract %O["y"] : !hw.struct<x: i1, y: i1>
    %4 = hw.struct_extract %a["x"] : !hw.struct<x: i1, y: i1>
    %5 = hw.struct_extract %a["y"] : !hw.struct<x: i1, y: i1>
}
hw.module @Top(%I: !hw.struct<x: i1, y: i1>) -> (O: !hw.struct<x: i1, y: i1>) {
    %0 = hw.instance "middle" @Middle(I: %I: !hw.struct<x: i1, y: i1>) -> (O: !hw.struct<x: i1, y: i1>)
    %2 = sv.xmr "middle", "bind_value_0" : !hw.inout<!hw.struct<x: i1, y: i1>>
    %1 = sv.read_inout %2 : !hw.inout<!hw.struct<x: i1, y: i1>>
    %4 = sv.xmr "middle", "bind_value_1" : !hw.inout<i1>
    %3 = sv.read_inout %4 : !hw.inout<i1>
    hw.instance "TopXMRAsserts_mlir_inst0" sym @TopXMRAsserts_mlir_inst0 @TopXMRAsserts_mlir(I: %I: !hw.struct<x: i1, y: i1>, O: %0: !hw.struct<x: i1, y: i1>, a: %1: !hw.struct<x: i1, y: i1>, b: %3: i1) -> () {doNotPrint = 1}
    hw.output %0 : !hw.struct<x: i1, y: i1>
}
sv.bind #hw.innerNameRef<@Top::@TopXMRAsserts_mlir_inst0>
