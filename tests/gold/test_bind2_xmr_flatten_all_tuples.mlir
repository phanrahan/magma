module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @Bottom(%I_x: i1, %I_y: i1) -> (O_x: i1, O_y: i1) {
        hw.output %I_x, %I_y : i1, i1
    }
    hw.module @Middle(%I_x: i1, %I_y: i1) -> (O_x: i1, O_y: i1) {
        %0, %1 = hw.instance "bottom" @Bottom(I_x: %I_x: i1, I_y: %I_y: i1) -> (O_x: i1, O_y: i1)
        hw.output %0, %1 : i1, i1
    }
    hw.module @TopXMRAsserts_mlir(%I_x: i1, %I_y: i1, %O_x: i1, %O_y: i1, %a_x: i1, %a_y: i1, %b: i1) -> () {
    }
    hw.module @Top(%I_x: i1, %I_y: i1) -> (O_x: i1, O_y: i1) {
        %0, %1 = hw.instance "middle" @Middle(I_x: %I_x: i1, I_y: %I_y: i1) -> (O_x: i1, O_y: i1)
        %4 = sv.xmr "middle", "bottom", "O_x" : !hw.inout<i1>
        %2 = sv.read_inout %4 : !hw.inout<i1>
        %5 = sv.xmr "middle", "bottom", "O_y" : !hw.inout<i1>
        %3 = sv.read_inout %5 : !hw.inout<i1>
        %7 = sv.xmr "middle", "bottom", "I_x" : !hw.inout<i1>
        %6 = sv.read_inout %7 : !hw.inout<i1>
        hw.instance "TopXMRAsserts_mlir_inst0" sym @Top.TopXMRAsserts_mlir_inst0 @TopXMRAsserts_mlir(I_x: %I_x: i1, I_y: %I_y: i1, O_x: %0: i1, O_y: %1: i1, a_x: %2: i1, a_y: %3: i1, b: %6: i1) -> () {doNotPrint = 1}
        hw.output %0, %1 : i1, i1
    }
    sv.bind #hw.innerNameRef<@Top::@Top.TopXMRAsserts_mlir_inst0>
}
