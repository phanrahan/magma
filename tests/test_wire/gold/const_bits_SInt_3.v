module main (output signed [2:0] O);
wire signed [2:0] Buf_inst0_O;
Buf Buf_inst0 (.I({1'b0,1'b0,1'b1}), .O(Buf_inst0_O));
assign O = Buf_inst0_O;
endmodule

