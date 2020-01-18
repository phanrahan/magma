module FF(input I, output reg O, input CLK);
always @(posedge CLK) begin
  O <= I;
end
endmodule
module Main (input CLK, input I, output O);
FF FF_inst0(.CLK(CLK), .I(I), .O(O));

assert property (@(posedge CLK) I |-> ##1 O);

endmodule

