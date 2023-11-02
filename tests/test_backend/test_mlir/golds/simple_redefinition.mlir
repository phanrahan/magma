module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @simple_redefinition_module(in %a: i1, out y: i1) {
        hw.output %a : i1
    }
    hw.module @simple_redefinition(in %a: i1, out y: i1) {
        %0 = hw.instance "simple_redefinition_module_inst0" @simple_redefinition_module(a: %a: i1) -> (y: i1)
        %1 = hw.instance "simple_redefinition_module_inst1" @simple_redefinition_module(a: %0: i1) -> (y: i1)
        hw.output %1 : i1
    }
}
