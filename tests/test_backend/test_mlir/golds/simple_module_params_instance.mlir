module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @simple_module_params<width: i32, height: i32>(in %I: i1, out O: i1) {
        hw.output %I : i1
    }
    hw.module @simple_module_params_instance(in %I: i1, out O: i1) {
        %0 = hw.instance "simple_module_params_inst0" @simple_module_params<width: i32 = 10, height: i32 = 20>(I: %I: i1) -> (O: i1)
        hw.output %0 : i1
    }
}
