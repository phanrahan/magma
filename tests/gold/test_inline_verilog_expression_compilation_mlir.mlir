module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @MyWrapperGen_1(%I: i1, %CLK: i1) -> (O: i1) {
        %0 = sv.verbatim.expr "R | I" () : () -> (i1)
        %2 = sv.wire sym @MyWrapperGen_1._magma_inline_wire0 {name="_magma_inline_wire0"} : !hw.inout<i1>
        sv.assign %2, %I : i1
        %1 = sv.read_inout %2 : !hw.inout<i1>
        sv.verbatim "reg [0:0] R;\nasssign R <= {{0}};\n" (%1) : i1
        hw.output %0 : i1
    }
    hw.module @MyWrapperGen_2(%I: i2, %CLK: i1) -> (O: i2) {
        %0 = sv.verbatim.expr "R | I" () : () -> (i2)
        %2 = sv.wire sym @MyWrapperGen_2._magma_inline_wire0 {name="_magma_inline_wire0"} : !hw.inout<i2>
        sv.assign %2, %I : i2
        %1 = sv.read_inout %2 : !hw.inout<i2>
        sv.verbatim "reg [1:0] R;\nasssign R <= {{0}};\n" (%1) : i2
        hw.output %0 : i2
    }
    hw.module @Top(%I: i2, %CLK: i1) -> (O: i2) {
        %0 = comb.extract %I from 0 : (i2) -> i1
        %1 = comb.concat %0 : i1
        %2 = hw.instance "MyWrapperGen_1_inst0" @MyWrapperGen_1(I: %1: i1, CLK: %CLK: i1) -> (O: i1)
        %3 = comb.extract %2 from 0 : (i1) -> i1
        %4 = comb.concat %3, %3 : i1, i1
        %5 = hw.instance "MyWrapperGen_2_inst0" @MyWrapperGen_2(I: %4: i2, CLK: %CLK: i1) -> (O: i2)
        hw.output %5 : i2
    }
}
