module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module.extern @InnerInnerDelayUnit(in %INPUT_0_data: i5, in %INPUT_0_valid: i1, in %INPUT_1_data: i5, in %INPUT_1_valid: i1, in %OUTPUT_0_ready: i1, in %OUTPUT_1_ready: i1, out INPUT_0_ready: i1, out INPUT_1_ready: i1, out OUTPUT_0_data: i5, out OUTPUT_0_valid: i1, out OUTPUT_1_data: i5, out OUTPUT_1_valid: i1)
    hw.module @InnerDelayUnit(in %INPUT_0_data: i5, in %INPUT_0_valid: i1, in %INPUT_1_data: i5, in %INPUT_1_valid: i1, in %OUTPUT_0_ready: i1, in %OUTPUT_1_ready: i1, in %CLK: i1, out INPUT_0_ready: i1, out INPUT_1_ready: i1, out OUTPUT_0_data: i5, out OUTPUT_0_valid: i1, out OUTPUT_1_data: i5, out OUTPUT_1_valid: i1) {
        %0, %1, %2, %3, %4, %5 = hw.instance "inner_inner_delay" @InnerInnerDelayUnit(INPUT_0_data: %INPUT_1_data: i5, INPUT_0_valid: %INPUT_1_valid: i1, INPUT_1_data: %INPUT_0_data: i5, INPUT_1_valid: %INPUT_0_valid: i1, OUTPUT_0_ready: %OUTPUT_1_ready: i1, OUTPUT_1_ready: %OUTPUT_0_ready: i1) -> (INPUT_0_ready: i1, INPUT_1_ready: i1, OUTPUT_0_data: i5, OUTPUT_0_valid: i1, OUTPUT_1_data: i5, OUTPUT_1_valid: i1)
        hw.output %1, %0, %4, %5, %2, %3 : i1, i1, i5, i1, i5, i1
    }
    hw.module @DelayUnit(in %INPUT_0_data: i5, in %INPUT_0_valid: i1, in %INPUT_1_data: i5, in %INPUT_1_valid: i1, in %OUTPUT_0_ready: i1, in %OUTPUT_1_ready: i1, in %CLK: i1, out INPUT_0_ready: i1, out INPUT_1_ready: i1, out OUTPUT_0_data: i5, out OUTPUT_0_valid: i1, out OUTPUT_1_data: i5, out OUTPUT_1_valid: i1) {
        %0, %1, %2, %3, %4, %5 = hw.instance "inner_delay" @InnerDelayUnit(INPUT_0_data: %INPUT_1_data: i5, INPUT_0_valid: %INPUT_1_valid: i1, INPUT_1_data: %INPUT_0_data: i5, INPUT_1_valid: %INPUT_0_valid: i1, OUTPUT_0_ready: %OUTPUT_1_ready: i1, OUTPUT_1_ready: %OUTPUT_0_ready: i1, CLK: %CLK: i1) -> (INPUT_0_ready: i1, INPUT_1_ready: i1, OUTPUT_0_data: i5, OUTPUT_0_valid: i1, OUTPUT_1_data: i5, OUTPUT_1_valid: i1)
        hw.output %1, %0, %4, %5, %2, %3 : i1, i1, i5, i1, i5, i1
    }
    hw.module @inline_verilog2_tuple(in %I_0_data: i5, in %I_0_valid: i1, in %I_1_data: i5, in %I_1_valid: i1, in %O_0_ready: i1, in %O_1_ready: i1, in %CLK: i1, out I_0_ready: i1, out I_1_ready: i1, out O_0_data: i5, out O_0_valid: i1, out O_1_data: i5, out O_1_valid: i1) {
        %0, %1, %2, %3, %4, %5 = hw.instance "DelayUnit_inst0" @DelayUnit(INPUT_0_data: %I_1_data: i5, INPUT_0_valid: %I_1_valid: i1, INPUT_1_data: %I_0_data: i5, INPUT_1_valid: %I_0_valid: i1, OUTPUT_0_ready: %O_1_ready: i1, OUTPUT_1_ready: %O_0_ready: i1, CLK: %CLK: i1) -> (INPUT_0_ready: i1, INPUT_1_ready: i1, OUTPUT_0_data: i5, OUTPUT_0_valid: i1, OUTPUT_1_data: i5, OUTPUT_1_valid: i1)
        sv.verbatim "assert property (@(posedge CLK) {{0}} |-> ##3 {{1}});" (%I_0_valid, %O_1_ready) : i1, i1
        sv.verbatim "assert property (@(posedge CLK) {{0}} |-> ##3 {{1}});" (%5, %0) : i1, i1
        %7 = sv.xmr "DelayUnit_inst0", "inner_delay", "OUTPUT_0_valid" : !hw.inout<i1>
        %6 = sv.read_inout %7 : !hw.inout<i1>
        %9 = sv.xmr "DelayUnit_inst0", "inner_delay", "INPUT_1_ready" : !hw.inout<i1>
        %8 = sv.read_inout %9 : !hw.inout<i1>
        sv.verbatim "assert property (@(posedge CLK) {{0}} |-> ##3 {{1}});" (%6, %8) : i1, i1
        %11 = sv.xmr "DelayUnit_inst0", "inner_delay", "inner_inner_delay", "OUTPUT_0_valid" : !hw.inout<i1>
        %10 = sv.read_inout %11 : !hw.inout<i1>
        %13 = sv.xmr "DelayUnit_inst0", "inner_delay", "inner_inner_delay", "INPUT_1_ready" : !hw.inout<i1>
        %12 = sv.read_inout %13 : !hw.inout<i1>
        sv.verbatim "assert property (@(posedge CLK) {{0}} |-> ##3 {{1}});" (%10, %12) : i1, i1
        hw.output %1, %0, %4, %5, %2, %3 : i1, i1, i5, i1, i5, i1
    }
}
