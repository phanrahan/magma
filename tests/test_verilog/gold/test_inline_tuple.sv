// Module `InnerInnerDelayUnit` defined externally
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
wire _magma_inline_wire4;
wire _magma_inline_wire5;
assign _magma_inline_wire4 = OUTPUT_1_valid;
assign _magma_inline_wire5 = INPUT_0_ready;
corebit_term corebit_term_inst0 (
    .in(_magma_inline_wire4)
);
corebit_term corebit_term_inst1 (
    .in(_magma_inline_wire5)
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
wire _magma_inline_wire2;
wire _magma_inline_wire3;
assign _magma_inline_wire2 = OUTPUT_1_valid;
assign _magma_inline_wire3 = INPUT_0_ready;
corebit_term corebit_term_inst0 (
    .in(_magma_inline_wire2)
);
corebit_term corebit_term_inst1 (
    .in(_magma_inline_wire3)
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
wire _magma_inline_wire0;
wire _magma_inline_wire1;
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
assign _magma_inline_wire0 = O_0_valid;
assign _magma_inline_wire1 = I_1_ready;
corebit_term corebit_term_inst0 (
    .in(_magma_inline_wire0)
);
corebit_term corebit_term_inst1 (
    .in(_magma_inline_wire1)
);
assert property (@(posedge CLK) I_0_valid |-> ##3 O_1_ready);

assert property (@(posedge CLK) _magma_inline_wire0 |-> ##3 _magma_inline_wire1);

assert property (@(posedge CLK) DelayUnit_inst0.inner_delay._magma_inline_wire2 |-> ##3 DelayUnit_inst0.inner_delay._magma_inline_wire3);

assert property (@(posedge CLK) DelayUnit_inst0.inner_delay.inner_inner_delay._magma_inline_wire4 |-> ##3 DelayUnit_inst0.inner_delay.inner_inner_delay._magma_inline_wire5);
endmodule

