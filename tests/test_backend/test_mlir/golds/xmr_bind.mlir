module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @xmr_bind_grandchild(in %a: i16, out y: i16) {
        hw.output %a : i16
    }
    hw.module @xmr_bind_child(in %a: i16, out y: i16) {
        %0 = hw.instance "xmr_bind_grandchild_inst0" @xmr_bind_grandchild(a: %a: i16) -> (y: i16)
        hw.output %0 : i16
    }
    hw.module @xmr_bind_asserts(in %a: i16, in %y: i16, in %other: i16) attributes {output_filelist = #hw.output_filelist<"xmr_bind_bind_files.list">} {
        sv.verbatim "assert property ({{0}} == 0);" (%other) : i16
    }
    hw.module @xmr_bind(in %a: i16, out y: i16) {
        %0 = hw.instance "xmr_bind_child_inst0" @xmr_bind_child(a: %a: i16) -> (y: i16)
        %2 = sv.xmr "xmr_bind_child_inst0", "xmr_bind_grandchild_inst0", "y" : !hw.inout<i16>
        %1 = sv.read_inout %2 : !hw.inout<i16>
        hw.instance "xmr_bind_asserts_inst0" sym @xmr_bind.xmr_bind_asserts_inst0 @xmr_bind_asserts(a: %a: i16, y: %0: i16, other: %1: i16) -> () {doNotPrint = true}
        hw.output %0 : i16
    }
    sv.bind #hw.innerNameRef<@xmr_bind::@xmr_bind.xmr_bind_asserts_inst0>
}
