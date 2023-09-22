module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @complex_inline_verilog(%I: i12, %CLK: i1) -> (O: i12) {
        %1 = sv.reg name "Register_inst0" : !hw.inout<i12>
        sv.alwaysff(posedge %CLK) {
            sv.passign %1, %I : i12
        }
        %2 = hw.constant 0 : i12
        sv.initial {
            sv.bpassign %1, %2 : i12
        }
        %0 = sv.read_inout %1 : !hw.inout<i12>
        %3 = comb.extract %I from 0 : (i12) -> i1
        %4 = comb.extract %0 from 0 : (i12) -> i1
        %5 = comb.extract %I from 1 : (i12) -> i1
        %6 = comb.extract %0 from 1 : (i12) -> i1
        %7 = comb.extract %I from 2 : (i12) -> i1
        %8 = comb.extract %0 from 2 : (i12) -> i1
        %9 = comb.extract %I from 3 : (i12) -> i1
        %10 = comb.extract %0 from 3 : (i12) -> i1
        %11 = comb.extract %I from 4 : (i12) -> i1
        %12 = comb.extract %0 from 4 : (i12) -> i1
        %13 = comb.extract %I from 5 : (i12) -> i1
        %14 = comb.extract %0 from 5 : (i12) -> i1
        %15 = comb.extract %I from 6 : (i12) -> i1
        %16 = comb.extract %0 from 6 : (i12) -> i1
        %17 = comb.extract %I from 7 : (i12) -> i1
        %18 = comb.extract %0 from 7 : (i12) -> i1
        %19 = comb.extract %I from 8 : (i12) -> i1
        %20 = comb.extract %0 from 8 : (i12) -> i1
        %21 = comb.extract %I from 9 : (i12) -> i1
        %22 = comb.extract %0 from 9 : (i12) -> i1
        %23 = comb.extract %I from 10 : (i12) -> i1
        %24 = comb.extract %0 from 10 : (i12) -> i1
        %25 = comb.extract %I from 11 : (i12) -> i1
        %26 = comb.extract %0 from 11 : (i12) -> i1
        sv.verbatim "assert property (@(posedge CLK) {{0}} |-> ##1 {{1}});\nassert property (@(posedge CLK) {{2}} |-> ##1 {{3}});\nassert property (@(posedge CLK) {{4}} |-> ##1 {{5}});\nassert property (@(posedge CLK) {{6}} |-> ##1 {{7}});\nassert property (@(posedge CLK) {{8}} |-> ##1 {{9}});\nassert property (@(posedge CLK) {{10}} |-> ##1 {{11}});\nassert property (@(posedge CLK) {{12}} |-> ##1 {{13}});\nassert property (@(posedge CLK) {{14}} |-> ##1 {{15}});\nassert property (@(posedge CLK) {{16}} |-> ##1 {{17}});\nassert property (@(posedge CLK) {{18}} |-> ##1 {{19}});\nassert property (@(posedge CLK) {{20}} |-> ##1 {{21}});\nassert property (@(posedge CLK) {{22}} |-> ##1 {{23}});" (%3, %4, %5, %6, %7, %8, %9, %10, %11, %12, %13, %14, %15, %16, %17, %18, %19, %20, %21, %22, %23, %24, %25, %26) : i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1
        sv.verbatim "// A fun{k}y comment with {{0}}" (%I) : i12
        hw.output %0 : i12
    }
}
