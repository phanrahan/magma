module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @Bottom(in %I_x: i1, in %I_y: i1, out O_x: i1, out O_y: i1, out x_0: i1, out x_1: i8) {
        %0 = hw.constant 0 : i1
        %1 = hw.constant 0 : i8
        hw.output %I_x, %I_y, %0, %1 : i1, i1, i1, i8
    }
    hw.module @Middle(in %I_x: i1, in %I_y: i1, out O_x: i1, out O_y: i1) {
        %0, %1, %2, %3 = hw.instance "bottom" @Bottom(I_x: %I_x: i1, I_y: %I_y: i1) -> (O_x: i1, O_y: i1, x_0: i1, x_1: i8)
        hw.output %0, %1 : i1, i1
    }
    hw.module @TopXMRAsserts_mlir(in %I_x: i1, in %I_y: i1, in %O_x: i1, in %O_y: i1, in %a_x: i1, in %a_y: i1, in %b: i1, in %c: i1) attributes {output_filelist = #hw.output_filelist<"$cwd/build/test_bind2_xmr_flatten_all_tuples_bind_files.list">} {
    }
    hw.module @Top(in %I_x: i1, in %I_y: i1, out O_x: i1, out O_y: i1) {
        %0, %1 = hw.instance "middle" @Middle(I_x: %I_x: i1, I_y: %I_y: i1) -> (O_x: i1, O_y: i1)
        %4 = sv.xmr "middle", "bottom", "O_x" : !hw.inout<i1>
        %2 = sv.read_inout %4 : !hw.inout<i1>
        %5 = sv.xmr "middle", "bottom", "O_y" : !hw.inout<i1>
        %3 = sv.read_inout %5 : !hw.inout<i1>
        %7 = sv.xmr "middle", "bottom", "I_x" : !hw.inout<i1>
        %6 = sv.read_inout %7 : !hw.inout<i1>
        %9 = sv.xmr "middle", "bottom", "x_0" : !hw.inout<i1>
        %8 = sv.read_inout %9 : !hw.inout<i1>
        hw.instance "TopXMRAsserts_mlir_inst0" sym @Top.TopXMRAsserts_mlir_inst0 @TopXMRAsserts_mlir(I_x: %I_x: i1, I_y: %I_y: i1, O_x: %0: i1, O_y: %1: i1, a_x: %2: i1, a_y: %3: i1, b: %6: i1, c: %8: i1) -> () {doNotPrint = true}
        hw.output %0, %1 : i1, i1
    }
    sv.bind #hw.innerNameRef<@Top::@Top.TopXMRAsserts_mlir_inst0>
}
