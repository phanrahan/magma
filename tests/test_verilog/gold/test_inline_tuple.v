// Module `InnerDelayUnit` defined externally
module DelayUnit (input CLK, input [4:0] INPUT_data, output INPUT_ready, input INPUT_valid, output [4:0] OUTPUT_data, input OUTPUT_ready, output OUTPUT_valid);
wire inner_delay_INPUT_ready;
wire [4:0] inner_delay_OUTPUT_data;
wire inner_delay_OUTPUT_valid;
InnerDelayUnit inner_delay(.INPUT_data(INPUT_data), .INPUT_ready(inner_delay_INPUT_ready), .INPUT_valid(INPUT_valid), .OUTPUT_data(inner_delay_OUTPUT_data), .OUTPUT_ready(OUTPUT_ready), .OUTPUT_valid(inner_delay_OUTPUT_valid));
assign INPUT_ready = inner_delay_INPUT_ready;
assign OUTPUT_data = inner_delay_OUTPUT_data;
assign OUTPUT_valid = inner_delay_OUTPUT_valid;
endmodule

module Main (input CLK, input [4:0] I_data, output I_ready, input I_valid, output [4:0] O_data, input O_ready, output O_valid);
wire DelayUnit_inst0_INPUT_ready;
wire [4:0] DelayUnit_inst0_OUTPUT_data;
wire DelayUnit_inst0_OUTPUT_valid;
DelayUnit DelayUnit_inst0(.CLK(CLK), .INPUT_data(I_data), .INPUT_ready(DelayUnit_inst0_INPUT_ready), .INPUT_valid(I_valid), .OUTPUT_data(DelayUnit_inst0_OUTPUT_data), .OUTPUT_ready(O_ready), .OUTPUT_valid(DelayUnit_inst0_OUTPUT_valid));
assign I_ready = DelayUnit_inst0_INPUT_ready;
assign O_data = DelayUnit_inst0_OUTPUT_data;
assign O_valid = DelayUnit_inst0_OUTPUT_valid;
assert property { @(posedge CLK) I_valid |-> ##3 O_ready };

assert property { @(posedge CLK) DelayUnit_inst0.INPUT_valid |-> ##3 DelayUnit_inst0.OUTPUT_ready };

assert property { @(posedge CLK) DelayUnit_inst0inner_delay.inner_delay.INPUT.inner_delay.INPUT_valid |-> ##3 DelayUnit_inst0inner_delay.inner_delay.OUTPUT.inner_delay.OUTPUT_ready };
endmodule

