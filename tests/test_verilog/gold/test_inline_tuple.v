module DelayUnit(
    input CLK,
    input [4:0] data_in,
    input valid_in,
    output reg ready_in,
    output reg [4:0] data_out,
    output reg valid_out,
    input ready_out
);
reg [1:0] count;

initial begin
  count = 0;
end

assign valid_out = count == 2'b11;
assign ready_in = count == 2'b10;
assign data_out = data_in;

always @(posedge CLK) begin
  if (count == 2'b10) begin
    count <= count + {2'b0, valid_in};
  end else if (count == 2'b11) begin
    count <= count + {2'b0, ready_in};
  end else begin
    count <= count + 1;
  end
end
endmodule
module Main (input CLK, input [4:0] I_data, output I_ready, input I_valid, output [4:0] O_data, input O_ready, output O_valid);
wire [4:0] DelayUnit_inst0_data_out;
wire DelayUnit_inst0_ready_in;
wire DelayUnit_inst0_valid_out;
DelayUnit DelayUnit_inst0(.CLK(CLK), .data_in(I_data), .data_out(DelayUnit_inst0_data_out), .ready_in(DelayUnit_inst0_ready_in), .ready_out(O_ready), .valid_in(I_valid), .valid_out(DelayUnit_inst0_valid_out));
assign I_ready = DelayUnit_inst0_ready_in;
assign O_data = DelayUnit_inst0_data_out;
assign O_valid = DelayUnit_inst0_valid_out;

assert property { @(posedge CLK) I_valid |-> ##3 O_ready };

endmodule

