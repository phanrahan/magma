hw.module @simple_inline_verilog_inline_verilog_0(%I: i1) -> () {
    sv.verbatim "\n\t// This is a comment.\n"
}
hw.module @simple_inline_verilog(%I: i1) -> (%O: i1) {
    %0 = hw.constant 0 : i1
    hw.instance "simple_inline_verilog_inline_verilog_inst_0" @simple_inline_verilog_inline_verilog_0(%0) : (i1) -> ()
    hw.output %I : i1
}
