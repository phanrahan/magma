module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @no_outputs(%I: i1) -> () {
        %1 = hw.constant -1 : i1
        %0 = comb.xor %1, %I : i1
    }
    hw.module @simple_side_effect_instance(%I: i1) -> (O: i1) {
        hw.instance "no_outputs_inst0" @no_outputs(I: %I: i1) -> ()
        hw.output %I : i1
    }
}
