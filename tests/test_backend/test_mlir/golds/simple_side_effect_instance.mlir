module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @no_outputs(in %I: i1) {
        %1 = hw.constant -1 : i1
        %0 = comb.xor %1, %I : i1
    }
    hw.module @simple_side_effect_instance(in %I: i1, out O: i1) {
        hw.instance "no_outputs_inst0" @no_outputs(I: %I: i1) -> ()
        hw.output %I : i1
    }
}
