// Module `InnerInnerDelayUnit` defined externally
module corebit_undriven (
    output out
);

endmodule

module corebit_term (
    input in
);

endmodule

module InnerDelayUnit (
    input CLK,
    input [4:0] INPUT_0_data,
    output INPUT_0_ready,
    input INPUT_0_valid,
    input [4:0] INPUT_1_data,
    output INPUT_1_ready,
    input INPUT_1_valid,
    output [4:0] OUTPUT_0_data,
    input OUTPUT_0_ready,
    output OUTPUT_0_valid,
    output [4:0] OUTPUT_1_data,
    input OUTPUT_1_ready,
    output OUTPUT_1_valid
);
InnerInnerDelayUnit inner_inner_delay (
    .INPUT_0_data(INPUT_1_data),
    .INPUT_0_ready(INPUT_1_ready),
    .INPUT_0_valid(INPUT_1_valid),
    .INPUT_1_data(INPUT_0_data),
    .INPUT_1_ready(INPUT_0_ready),
    .INPUT_1_valid(INPUT_0_valid),
    .OUTPUT_0_data(OUTPUT_1_data),
    .OUTPUT_0_ready(OUTPUT_1_ready),
    .OUTPUT_0_valid(OUTPUT_1_valid),
    .OUTPUT_1_data(OUTPUT_0_data),
    .OUTPUT_1_ready(OUTPUT_0_ready),
    .OUTPUT_1_valid(OUTPUT_0_valid)
);
endmodule

module InlineVerilogc466ffeffb5b4540b56f0a9267c4197c___magma_inline_value_0_Main_I_1_valid___magma_inline_value_1_DelayUnit_inst0_inner_delay_inner_delay_OUTPUT_1_ready (
    input __magma_inline_value_0,
    output __magma_inline_value_1
);
corebit_term corebit_term_inst0 (
    .in(__magma_inline_value_0)
);
corebit_undriven corebit_undriven_inst0 (
    .out(__magma_inline_value_1)
);
assert property (@(posedge CLK) __magma_inline_value_0 |-> ##3 __magma_inline_value_1);
endmodule

module InlineVerilogc466ffeffb5b4540b56f0a9267c4197c___magma_inline_value_0_Main_I_0_valid___magma_inline_value_1_Main_O_1_ready (
    input __magma_inline_value_0,
    input __magma_inline_value_1
);
corebit_term corebit_term_inst0 (
    .in(__magma_inline_value_0)
);
corebit_term corebit_term_inst1 (
    .in(__magma_inline_value_1)
);
assert property (@(posedge CLK) __magma_inline_value_0 |-> ##3 __magma_inline_value_1);
endmodule

module InlineVerilogc466ffeffb5b4540b56f0a9267c4197c___magma_inline_value_0_DelayUnit_inst0_inner_delay_inner_inner_delay_inner_inner_delay_INPUT_0_valid___magma_inline_value_1_DelayUnit_inst0_inner_delay_inner_inner_delay_inner_inner_delay_OUTPUT_1_ready (
    output __magma_inline_value_0,
    output __magma_inline_value_1
);
corebit_undriven corebit_undriven_inst0 (
    .out(__magma_inline_value_0)
);
corebit_undriven corebit_undriven_inst1 (
    .out(__magma_inline_value_1)
);
assert property (@(posedge CLK) __magma_inline_value_0 |-> ##3 __magma_inline_value_1);
endmodule

module DelayUnit (
    input CLK,
    input [4:0] INPUT_0_data,
    output INPUT_0_ready,
    input INPUT_0_valid,
    input [4:0] INPUT_1_data,
    output INPUT_1_ready,
    input INPUT_1_valid,
    output [4:0] OUTPUT_0_data,
    input OUTPUT_0_ready,
    output OUTPUT_0_valid,
    output [4:0] OUTPUT_1_data,
    input OUTPUT_1_ready,
    output OUTPUT_1_valid
);
InnerDelayUnit inner_delay (
    .CLK(CLK),
    .INPUT_0_data(INPUT_1_data),
    .INPUT_0_ready(INPUT_1_ready),
    .INPUT_0_valid(INPUT_1_valid),
    .INPUT_1_data(INPUT_0_data),
    .INPUT_1_ready(INPUT_0_ready),
    .INPUT_1_valid(INPUT_0_valid),
    .OUTPUT_0_data(OUTPUT_1_data),
    .OUTPUT_0_ready(OUTPUT_1_ready),
    .OUTPUT_0_valid(OUTPUT_1_valid),
    .OUTPUT_1_data(OUTPUT_0_data),
    .OUTPUT_1_ready(OUTPUT_0_ready),
    .OUTPUT_1_valid(OUTPUT_0_valid)
);
endmodule

module Main (
    input CLK,
    input [4:0] I_0_data,
    output I_0_ready,
    input I_0_valid,
    input [4:0] I_1_data,
    output I_1_ready,
    input I_1_valid,
    output [4:0] O_0_data,
    input O_0_ready,
    output O_0_valid,
    output [4:0] O_1_data,
    input O_1_ready,
    output O_1_valid
);
wire InlineVerilogc466ffeffb5b4540b56f0a9267c4197c___magma_inline_value_0_DelayUnit_inst0_inner_delay_inner_inner_delay_inner_inner_delay_INPUT_0_valid___magma_inline_value_1_DelayUnit_inst0_inner_delay_inner_inner_delay_inner_inner_delay_OUTPUT_1_ready_inst0___magma_inline_value_0;
wire InlineVerilogc466ffeffb5b4540b56f0a9267c4197c___magma_inline_value_0_DelayUnit_inst0_inner_delay_inner_inner_delay_inner_inner_delay_INPUT_0_valid___magma_inline_value_1_DelayUnit_inst0_inner_delay_inner_inner_delay_inner_inner_delay_OUTPUT_1_ready_inst0___magma_inline_value_1;
wire InlineVerilogc466ffeffb5b4540b56f0a9267c4197c___magma_inline_value_0_Main_I_1_valid___magma_inline_value_1_DelayUnit_inst0_inner_delay_inner_delay_OUTPUT_1_ready_inst0___magma_inline_value_1;
DelayUnit DelayUnit_inst0 (
    .CLK(CLK),
    .INPUT_0_data(I_1_data),
    .INPUT_0_ready(I_1_ready),
    .INPUT_0_valid(I_1_valid),
    .INPUT_1_data(I_0_data),
    .INPUT_1_ready(I_0_ready),
    .INPUT_1_valid(I_0_valid),
    .OUTPUT_0_data(O_1_data),
    .OUTPUT_0_ready(O_1_ready),
    .OUTPUT_0_valid(O_1_valid),
    .OUTPUT_1_data(O_0_data),
    .OUTPUT_1_ready(O_0_ready),
    .OUTPUT_1_valid(O_0_valid)
);
InlineVerilogc466ffeffb5b4540b56f0a9267c4197c___magma_inline_value_0_DelayUnit_inst0_inner_delay_inner_inner_delay_inner_inner_delay_INPUT_0_valid___magma_inline_value_1_DelayUnit_inst0_inner_delay_inner_inner_delay_inner_inner_delay_OUTPUT_1_ready InlineVerilogc466ffeffb5b4540b56f0a9267c4197c___magma_inline_value_0_DelayUnit_inst0_inner_delay_inner_inner_delay_inner_inner_delay_INPUT_0_valid___magma_inline_value_1_DelayUnit_inst0_inner_delay_inner_inner_delay_inner_inner_delay_OUTPUT_1_ready_inst0 (
    .__magma_inline_value_0(InlineVerilogc466ffeffb5b4540b56f0a9267c4197c___magma_inline_value_0_DelayUnit_inst0_inner_delay_inner_inner_delay_inner_inner_delay_INPUT_0_valid___magma_inline_value_1_DelayUnit_inst0_inner_delay_inner_inner_delay_inner_inner_delay_OUTPUT_1_ready_inst0___magma_inline_value_0),
    .__magma_inline_value_1(InlineVerilogc466ffeffb5b4540b56f0a9267c4197c___magma_inline_value_0_DelayUnit_inst0_inner_delay_inner_inner_delay_inner_inner_delay_INPUT_0_valid___magma_inline_value_1_DelayUnit_inst0_inner_delay_inner_inner_delay_inner_inner_delay_OUTPUT_1_ready_inst0___magma_inline_value_1)
);
InlineVerilogc466ffeffb5b4540b56f0a9267c4197c___magma_inline_value_0_Main_I_0_valid___magma_inline_value_1_Main_O_1_ready InlineVerilogc466ffeffb5b4540b56f0a9267c4197c___magma_inline_value_0_Main_I_0_valid___magma_inline_value_1_Main_O_1_ready_inst0 (
    .__magma_inline_value_0(I_0_valid),
    .__magma_inline_value_1(O_1_ready)
);
InlineVerilogc466ffeffb5b4540b56f0a9267c4197c___magma_inline_value_0_Main_I_0_valid___magma_inline_value_1_Main_O_1_ready InlineVerilogc466ffeffb5b4540b56f0a9267c4197c___magma_inline_value_0_Main_I_0_valid___magma_inline_value_1_Main_O_1_ready_inst1 (
    .__magma_inline_value_0(I_0_valid),
    .__magma_inline_value_1(O_1_ready)
);
InlineVerilogc466ffeffb5b4540b56f0a9267c4197c___magma_inline_value_0_Main_I_1_valid___magma_inline_value_1_DelayUnit_inst0_inner_delay_inner_delay_OUTPUT_1_ready InlineVerilogc466ffeffb5b4540b56f0a9267c4197c___magma_inline_value_0_Main_I_1_valid___magma_inline_value_1_DelayUnit_inst0_inner_delay_inner_delay_OUTPUT_1_ready_inst0 (
    .__magma_inline_value_0(I_1_valid),
    .__magma_inline_value_1(InlineVerilogc466ffeffb5b4540b56f0a9267c4197c___magma_inline_value_0_Main_I_1_valid___magma_inline_value_1_DelayUnit_inst0_inner_delay_inner_delay_OUTPUT_1_ready_inst0___magma_inline_value_1)
);
endmodule

