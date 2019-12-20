module FF(input I, output O, input CLK);
always @(posedge CLK) begin
  O <= I;
end
endmodule
module Main (input CLK, input I, output O);
wire FF_inst0_O;
FF FF_inst0(.CLK(CLK), .I(I), .O(FF_inst0_O));
assign O = FF_inst0_O;

assert property { @(posedge CLK) I |-> ##1 O };

endmodule

