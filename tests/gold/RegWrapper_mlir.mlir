hw.module @RegWrapper(%I: i1, %CLK: i1) -> (O: i1) {
    %0 = sv.verbatim.expr "R | I" () : () -> (i1)
    %2 = sv.wire sym @RegWrapper._magma_inline_wire0 {name="_magma_inline_wire0"} : !hw.inout<i1>
    sv.assign %2, %I : i1
    %1 = sv.read_inout %2 : !hw.inout<i1>
    sv.verbatim "reg [0:0] R;\nasssign R <= {{0}};\n" (%1) : i1
    hw.output %0 : i1
}
