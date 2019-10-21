// Module `FF` defined externally
module Top (input ASYNCRESET, input CLK, input [1:0] I, output [1:0] O);
wire FF_inst0_q;
wire FF_inst1_q;
FF #(.init(0)) FF_inst0(.clk(CLK), .d(I[0]), .q(FF_inst0_q), .rst(ASYNCRESET));
FF #(.init(1)) FF_inst1(.clk(CLK), .d(I[1]), .q(FF_inst1_q), .rst(ASYNCRESET));
assign O = {FF_inst1_q,FF_inst0_q};
endmodule

