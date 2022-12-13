module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @xmr_bind_grandchild(%a: i16) -> (y: i16) {
        hw.output %a : i16
    }
    hw.module @xmr_bind_child(%a: i16) -> (y: i16) {
        %0 = hw.instance "inst" @xmr_bind_grandchild(a: %a: i16) -> (y: i16)
        hw.output %0 : i16
    }
    hw.module @xmr_bind_asserts(%a: i16, %y: i16, %other: i16) -> () {
        sv.verbatim "assert property ({{0}} == 0);" (%other) : i16
    }
    hw.module @xmr_bind(%a: i16) -> (y: i16) {
        %0 = hw.instance "inst" @xmr_bind_child(a: %a: i16) -> (y: i16)
        %1 = sv.xmr "inst", "inst", "y" : !hw.inout<i16>
        %2 = sv.read_inout %1 : !hw.inout<i16>
        hw.instance "xmr_bind_asserts_inst" sym @xmr_bind.xmr_bind_asserts_inst @xmr_bind_asserts(a: %a: i16, y: %0: i16, other: %2: i16) -> () {doNotPrint = 1}
        hw.output %0 : i16
    }
    sv.bind #hw.innerNameRef<@xmr_bind::@xmr_bind.xmr_bind_asserts_inst>
}
