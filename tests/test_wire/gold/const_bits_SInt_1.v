module main (output signed [0:0] O);
wire signed [0:0] Buf_inst0_O;
Buf Buf_inst0 (.I({1'b1}), .O(Buf_inst0_O));
assign O = Buf_inst0_O;
endmodule

