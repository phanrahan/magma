hw.module @simple_comb(%a: i16, %b: i16, %c: i16) -> (y: i16, z: i16) {
    %1 = hw.constant -1 : i16
    %0 = comb.xor %1, %a : i16
    %2 = comb.or %a, %0 : i16
    %3 = comb.or %2, %b : i16
    hw.output %3, %3 : i16, i16
}
hw.module @simple_hierarchy(%a: i16, %b: i16, %c: i16) -> (y: i16, z: i16) {
    %0, %1 = hw.instance "simple_comb_inst0" @simple_comb(a: %a: i16, b: %b: i16, c: %c: i16) -> (y: i16, z: i16)
    hw.output %0, %1 : i16, i16
}
hw.module @xmr_bind_asserts(%a: i16, %b: i16, %c: i16, %y: i16, %z: i16, %a_inner: i16) -> () {
    %1 = sv.wire sym @xmr_bind_asserts._magma_inline_wire0 {name="_magma_inline_wire0"} : !hw.inout<i16>
    sv.assign %1, %a_inner : i16
    %0 = sv.read_inout %1 : !hw.inout<i16>
    sv.verbatim "assert property ({{0}} == 0);" (%0) : i16
}
hw.module @xmr_bind(%a: i16, %b: i16, %c: i16) -> (y: i16, z: i16) {
    %0, %1 = hw.instance "inst" @simple_hierarchy(a: %a: i16, b: %b: i16, c: %c: i16) -> (y: i16, z: i16)
    %2 = sv.xmr "inst", "simple_comb_inst0", "a" : !hw.inout<i16>
    %3 = sv.read_inout %2 : !hw.inout<i16>
    hw.instance "xmr_bind_asserts_inst" sym @xmr_bind.xmr_bind_asserts_inst @xmr_bind_asserts(a: %a: i16, b: %b: i16, c: %c: i16, y: %0: i16, z: %1: i16, a_inner: %3: i16) -> () {doNotPrint = 1}
    hw.output %0, %1 : i16, i16
}
sv.bind #hw.innerNameRef<@xmr_bind::@xmr_bind.xmr_bind_asserts_inst>
