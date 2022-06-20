hw.module @xmr_bind_grandchild(%a: i16) -> (y: i16) {
    hw.output %a : i16
}
hw.module @xmr_bind_child(%a: i16) -> (y: i16) {
    %0 = hw.instance "xmr_bind_grandchild_inst0" @xmr_bind_grandchild(a: %a: i16) -> (y: i16)
    hw.output %0 : i16
}
hw.module @xmr_bind_asserts(%a: i16, %y: i16, %other: i16, %that: i16) -> () {
    %1 = sv.wire sym @xmr_bind_asserts._magma_inline_wire0 {name="_magma_inline_wire0"} : !hw.inout<i16>
    sv.assign %1, %other : i16
    %0 = sv.read_inout %1 : !hw.inout<i16>
    %3 = sv.wire sym @xmr_bind_asserts._magma_inline_wire1 {name="_magma_inline_wire1"} : !hw.inout<i16>
    sv.assign %3, %that : i16
    %2 = sv.read_inout %3 : !hw.inout<i16>
    sv.verbatim "assert property ({{0}} == 0 && {{1}} == 0);" (%0, %2) : i16, i16
}
hw.module @xmr_bind(%a: i16) -> (y: i16) {
    %0 = hw.instance "xmr_bind_child_inst0" @xmr_bind_child(a: %a: i16) -> (y: i16)
    %1 = sv.xmr "xmr_bind_child_inst0", "xmr_bind_grandchild_inst0", "y" : !hw.inout<i16>
    %2 = sv.read_inout %1 : !hw.inout<i16>
    %3 = sv.xmr "y_value" : !hw.inout<i16>
    %4 = sv.read_inout %3 : !hw.inout<i16>
    hw.instance "xmr_bind_asserts_inst" sym @xmr_bind.xmr_bind_asserts_inst @xmr_bind_asserts(a: %a: i16, y: %0: i16, other: %2: i16, that: %4: i16) -> () {doNotPrint = 1}
    hw.output %0 : i16
}
sv.bind #hw.innerNameRef<@xmr_bind::@xmr_bind.xmr_bind_asserts_inst>
