module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @inline_verilog2_share_default_clocks(%x: i1, %y: i1, %CLK: i1, %RESET: i1) -> () {
        sv.verbatim "assert property (@(posedge {{0}}) disable iff (! {{1}}) {{2}} |-> ##1 {{3}});" (%CLK, %RESET, %x, %y) : i1, i1, i1, i1
        sv.verbatim "assert property (@(posedge {{0}}) disable iff (! {{1}}) {{2}} |-> ##1 {{3}});" (%CLK, %RESET, %x, %y) : i1, i1, i1, i1
    }
}
