// Module `FF` defined externally
module Top (input CLK, input I, output O);
wire FF_inst0_O;
wire FF_inst1_O;
FF #(.init(0)) FF_inst0(.CLK(CLK), .I(I), .O(FF_inst0_O));
FF #(.init(1)) FF_inst1(.CLK(CLK), .I(FF_inst0_O), .O(FF_inst1_O));
assign O = FF_inst1_O;
endmodule

