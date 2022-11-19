module Top (input [1:0] I, output [1:0] O, input  CLK, input  ASYNCRESET);
wire  ff0_q;
wire  ff1_q;
FF #(.init(0)) ff0 (.clk(CLK), .rst(ASYNCRESET), .d(I[0]), .q(ff0_q));
FF #(.init(1)) ff1 (.clk(CLK), .rst(ASYNCRESET), .d(I[1]), .q(ff1_q));
assign O = {ff1_q,ff0_q};
endmodule

