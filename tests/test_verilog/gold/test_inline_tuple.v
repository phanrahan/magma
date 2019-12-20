// Module `InnerDelayUnit` defined externally
module DelayUnit (input CLK, input [4:0] INPUT_0_data, output INPUT_0_ready, input INPUT_0_valid, input [4:0] INPUT_1_data, output INPUT_1_ready, input INPUT_1_valid, output [4:0] OUTPUT_0_data, input OUTPUT_0_ready, output OUTPUT_0_valid, output [4:0] OUTPUT_1_data, input OUTPUT_1_ready, output OUTPUT_1_valid);
wire inner_delay_INPUT_0_ready;
wire inner_delay_INPUT_1_ready;
wire [4:0] inner_delay_OUTPUT_0_data;
wire inner_delay_OUTPUT_0_valid;
wire [4:0] inner_delay_OUTPUT_1_data;
wire inner_delay_OUTPUT_1_valid;
InnerDelayUnit inner_delay(.INPUT_0_data(INPUT_1_data), .INPUT_0_ready(inner_delay_INPUT_0_ready), .INPUT_0_valid(INPUT_1_valid), .INPUT_1_data(INPUT_0_data), .INPUT_1_ready(inner_delay_INPUT_1_ready), .INPUT_1_valid(INPUT_0_valid), .OUTPUT_0_data(inner_delay_OUTPUT_0_data), .OUTPUT_0_ready(OUTPUT_1_ready), .OUTPUT_0_valid(inner_delay_OUTPUT_0_valid), .OUTPUT_1_data(inner_delay_OUTPUT_1_data), .OUTPUT_1_ready(OUTPUT_0_ready), .OUTPUT_1_valid(inner_delay_OUTPUT_1_valid));
assign INPUT_0_ready = inner_delay_INPUT_1_ready;
assign INPUT_1_ready = inner_delay_INPUT_0_ready;
assign OUTPUT_0_data = inner_delay_OUTPUT_1_data;
assign OUTPUT_0_valid = inner_delay_OUTPUT_1_valid;
assign OUTPUT_1_data = inner_delay_OUTPUT_0_data;
assign OUTPUT_1_valid = inner_delay_OUTPUT_0_valid;
endmodule

module Main (input CLK, input [4:0] I_0_data, output I_0_ready, input I_0_valid, input [4:0] I_1_data, output I_1_ready, input I_1_valid, output [4:0] O_0_data, input O_0_ready, output O_0_valid, output [4:0] O_1_data, input O_1_ready, output O_1_valid);
wire DelayUnit_inst0_INPUT_0_ready;
wire DelayUnit_inst0_INPUT_1_ready;
wire [4:0] DelayUnit_inst0_OUTPUT_0_data;
wire DelayUnit_inst0_OUTPUT_0_valid;
wire [4:0] DelayUnit_inst0_OUTPUT_1_data;
wire DelayUnit_inst0_OUTPUT_1_valid;
DelayUnit DelayUnit_inst0(.CLK(CLK), .INPUT_0_data(I_1_data), .INPUT_0_ready(DelayUnit_inst0_INPUT_0_ready), .INPUT_0_valid(I_1_valid), .INPUT_1_data(I_0_data), .INPUT_1_ready(DelayUnit_inst0_INPUT_1_ready), .INPUT_1_valid(I_0_valid), .OUTPUT_0_data(DelayUnit_inst0_OUTPUT_0_data), .OUTPUT_0_ready(O_1_ready), .OUTPUT_0_valid(DelayUnit_inst0_OUTPUT_0_valid), .OUTPUT_1_data(DelayUnit_inst0_OUTPUT_1_data), .OUTPUT_1_ready(O_0_ready), .OUTPUT_1_valid(DelayUnit_inst0_OUTPUT_1_valid));
assign I_0_ready = DelayUnit_inst0_INPUT_1_ready;
assign I_1_ready = DelayUnit_inst0_INPUT_0_ready;
assign O_0_data = DelayUnit_inst0_OUTPUT_1_data;
assign O_0_valid = DelayUnit_inst0_OUTPUT_1_valid;
assign O_1_data = DelayUnit_inst0_OUTPUT_0_data;
assign O_1_valid = DelayUnit_inst0_OUTPUT_0_valid;
assert property { @(posedge CLK) I_0_valid |-> ##3 O_1_ready };

assert property { @(posedge CLK) DelayUnit_inst0.INPUT_1_valid |-> ##3 DelayUnit_inst0.OUTPUT_0_ready };

assert property { @(posedge CLK) DelayUnit_inst0.inner_delay.INPUT_0_valid |-> ##3 DelayUnit_inst0.inner_delay.OUTPUT_1_ready };
endmodule

