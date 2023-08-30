module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @TopCompileGuardAsserts_mlir(%I: i1, %O: i1, %other: i1) -> () attributes {output_filelist = #hw.output_filelist<"$cwd/build/test_bind2_compile_guard_bind_files.list">} {
    }
    hw.module @Top(%I: i1) -> (O: i1) {
        %1 = hw.constant -1 : i1
        %0 = comb.xor %1, %I : i1
        hw.instance "TopCompileGuardAsserts_mlir_inst0" sym @Top.TopCompileGuardAsserts_mlir_inst0 @TopCompileGuardAsserts_mlir(I: %I: i1, O: %0: i1, other: %I: i1) -> () {doNotPrint = true}
        hw.output %0 : i1
    }
    sv.ifdef "ASSERT_ON" {
        sv.bind #hw.innerNameRef<@Top::@Top.TopCompileGuardAsserts_mlir_inst0>
    }
}
