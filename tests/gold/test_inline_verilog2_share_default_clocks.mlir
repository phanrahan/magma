module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @inline_verilog2_share_default_clocks(in %x: i1, in %y: i1, in %CLK: i1, in %RESET: i1) {
        sv.verbatim "assert property (@(posedge {{0}}) disable iff (! {{1}}) {{2}} |-> ##1 {{3}});" (%CLK, %RESET, %x, %y) : i1, i1, i1, i1
        sv.verbatim "assert property (@(posedge {{0}}) disable iff (! {{1}}) {{2}} |-> ##1 {{3}});" (%CLK, %RESET, %x, %y) : i1, i1, i1, i1
    }
}
