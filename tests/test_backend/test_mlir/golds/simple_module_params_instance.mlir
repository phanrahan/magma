module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @simple_module_params<width: i32, height: i32>(%I: i1) -> (O: i1) {
        hw.output %I : i1
    }
    hw.module @simple_module_params_instance(%I: i1) -> (O: i1) {
        %0 = hw.instance "simple_module_params_inst0" @simple_module_params<width: i32 = 10, height: i32 = 20>(I: %I: i1) -> (O: i1)
        hw.output %0 : i1
    }
}
